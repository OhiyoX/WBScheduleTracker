# -*- coding: utf-8 -*-
# @Time    : 7/27/2021 11:06 PM
# @Author  : Chris.Wang
# @Site    : 
# @File    : db.py
# @Software: PyCharm
# @Description:

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, INTEGER, CHAR, TEXT, DATETIME
from sqlalchemy.ext.declarative import declarative_base

import os.path

Base = declarative_base()
db_path = 'resource/database.db'


class FollowerLog(Base):
    __tablename__ = "followerlogs"

    id = Column(INTEGER(), nullable=False, autoincrement=True, primary_key=True)
    uid = Column(INTEGER(), nullable=False)
    alias_id = Column(CHAR(255), nullable=True)
    profile_image_url = Column(TEXT(),nullable=True)
    profile_url = Column(TEXT(),nullable=False)
    screen_name = Column(CHAR(255), nullable=False)
    followers_count = Column(INTEGER(),nullable=False)
    raw_data = Column(TEXT(), nullable=True)
    response_time = Column(DATETIME(), nullable=False)

class QueryTaskStack(Base):

    __tablename__ = 'querytaskstacks'
    uid = Column(INTEGER(),nullable=False,primary_key=True)
    screen_name = Column(CHAR(255),nullable=True)
    add_time = Column(DATETIME(),nullable=False)


def build_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print('successfully built database.')


def build_session(db_url):
    db_path = db_url.replace('sqlite:///','')
    if not os.path.exists(db_path):
        build_db(db_url)
    engine = create_engine(db_url)
    Session = sessionmaker()
    session = Session(bind=engine)
    return session

if __name__ == '__main__':
    # db_url = 'sqlite:///' + db_path
    # build_db(db_url)

    attr:list = list(filter(lambda x:not x.startswith('_'),FollowerLog.__dict__.keys()))
    print(attr)
