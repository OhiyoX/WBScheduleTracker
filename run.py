from bs4 import BeautifulSoup
import os
import json
import re
import time
import traceback

import function as func
from db import FollowerLog,QueryTaskStack,Base
from db import build_session
from datetime import datetime
from typing import Any

db_url = 'sqlite:///resource/database.db'
with open('config.json','r') as fp:
    config = json.load(fp)

if config['remote']:
    db_url=config['db_url']

def table_attr(Table:Base) -> list:
    return list(filter(lambda x:not x.startswith('_'),Table.__dict__.keys()))

class WeiboFans():
    def __init__(self):
        pass

    def get_uid_from_home(self):
        pass


    # 根据uid获取response
    def get_apidata(self, uid):
        """dict 形式"""
        prefix = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='
        # prefix_test = 'https://weibo.com/ajax/profile/info?uid='
        url = prefix + uid
        response = func.get_response(url)
        return response.text

    def get_uid_redirect_url(self, ref):
        # 当出现自定义域名时使用这个方法获取原始id，会出现跳转域名
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OP'
                          'D3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chr'
                          'ome/84.0.4147.89 Mobile Safari/537.36 Edg/84.0.522.48'
        }
        content = func.get_response(ref, headers=headers)
        uid = re.search('[0-9]+', content.url)
        return uid.group()

    def loop_crawl(self,uid_list:list):
        global detail
        for uid in uid_list:
            user_info = {}
            user_info_keys = table_attr(FollowerLog)
            user_info_keys = user_info_keys[1:] # skip id
            try:
                detail = self.get_apidata(uid)
            except Exception as err:
                print('遇到了错误。')
                print(err)
                traceback.print_exc()

            response_time = datetime.now()
            detail_json = json.loads(detail)
            if detail_json['ok'] == 0:
                return False
            else:
                user_info_data = detail_json['data']['userInfo']
                for k in user_info_keys:
                    user_info[k] = user_info_data[k] if k in user_info_data.keys() else ''
                user_info['raw_data'] = detail
                user_info['response_time'] = response_time

                new_log = FollowerLog(**user_info)
                session = build_session(db_url=db_url)
                try:
                    session.add(new_log)
                    session.commit()
                except Exception as err:
                    session.rollback()
                    print(err)
                    traceback.print_exc()
                    exit('数据库连接错误。')
                return True


    def add_query_task(self,**kwargs):
        avail = {}
        for k in kwargs.keys():
            if k in table_attr(QueryTaskStack):
                avail[k] = kwargs[k]
            else:
                avail[k] = ''
                print("无效属性，跳过")
        if avail['uid'] is None:
            exit('设置博主uid不能为空值')
        avail['add_time'] = datetime.now()
        session = build_session(db_url=db_url)
        new_task = QueryTaskStack(**avail)
        try:
            if session.query(QueryTaskStack.uid).filter_by(uid=avail['uid']).count() > 0:
                print('已存在相似任务。')
                return True
            session.add(new_task)
            session.commit()
        except Exception as err:
            session.rollback()
            print(err)
            traceback.print_exc()
            exit(-1)

    def add_batch_query_task(self):
        pass

    def del_query_task(self,**kwargs):
        pass


    def run(self):
        session = build_session(db_url=db_url)
        result = session.query(QueryTaskStack).all()
        uid_list = [str(r.uid) for r in result]
        self.loop_crawl(uid_list=uid_list)

if __name__ == '__main__':
    wf = WeiboFans()
    wf.run()
