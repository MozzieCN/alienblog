#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       shcema.py
#       
#       Copyright 2011 feiyd <feiyd000@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import time
from models import  *
from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String,create_engine,DateTime,Enum,Text
from sqlalchemy.orm import mapper, relationship,scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from config import db_prefix as prefix
#prefix='t'
print dir(time)
Base = declarative_base()
user = Table('%s_user'%(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('name',String(20),nullable=False),
            Column('password',String(50),nullable=False),
            Column('mail',String(60)),
            Column('url',String(100)),
            Column('displayName',String(80)),
            Column('createdTime',DateTime,default=func.now()),
            Column('status',String(10),nullable=False),
            Column('group',String(10),nullable=False),
            Column('authCode',String(30)),
            Column('lastip',String(20)),
            Column('lastlogin',DateTime)
            )
application = Table('%s_domain' %(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('domain',String(60),nullable=True)
            )
'''
slug= Table('%s_slug' %(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('appid',Integer,ForeignKey(application.c.id)),
            Column('name',String(40),nullable=False),
            Column('displayName',String(40),nullable=False)
            )
'''
archive = Table('%s_archive' %(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('appid',Integer,nullable=False),
            Column('type',String(10),default='post',nullable=False),
            Column('alias',String(100),nullable=False),
            Column('year',String(4),default=time.strftime('%Y'),nullable=False),
            Column('month',String(4),default=time.strftime('%m'),nullable=False),
            Column('day',String(4),default=time.strftime('%d'),nullable=False),
            Column('title',String(50),nullable=False),
            Column('desc',String(200),nullable=False),
            Column('content',Text),
            Column('attr',String(30)),
            Column('order', Integer,default=0),
            Column('authorid',Integer),
            Column('status',String(20),nullable=False,default='draft'),
            Column('password',String(50)),
            Column('allowComment',String(1),default='1'),
            Column('prent',Integer),
            Column('pubTime',DateTime,default=func.now()),
            Column('modifyTime',DateTime,default=func.now()),
            Column('commentCount',Integer),
            Column('keywords',String(30)),
            Column('click',Integer,default=0),
            Column('channel',String(20),default='website')
        )
'''
tag         = Table('%s_tag' %(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('appId',Integer,ForeignKey(application.c.id)),
            Column('archiveId',Integer,ForeignKey(archive.c.id)),
            Column('name',String(40),nullable=False),
            #Column('displayName',String(40),nullable=False),
            Column('click',Integer,default=0)
            )
'''
meta        = Table('%s_meta' %(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('name',String(40),nullable=False),
            Column('type',String(20),default='tag'),
            Column('click',Integer,default=0),
            Column('order',Integer,default=0)
            )
option  = Table('%s_option' %(prefix),Base.metadata,
            Column('appid',Integer, ForeignKey(application.c.id),primary_key=True),
            Column('key',String(20),primary_key=True),
            Column('value',String(40))
        )
relationship= Table('%s_relationship' %(prefix),Base.metadata,
            Column('cid',Integer,ForeignKey(archive.c.id),primary_key=True),
            Column('mid',Integer,ForeignKey(meta.c.id),primary_key=True),
            Column('appId',Integer,ForeignKey(application.c.id),primary_key=True)
        )
comment = Table('%s_comment'%(prefix),Base.metadata,
            Column('id',Integer,primary_key=True),
            Column('appid',Integer,ForeignKey(application.c.id),index=True),
            Column('parent',Integer,default=0),
            Column('created',DateTime,default=func.now()),
            Column('authorId',Integer),
            Column('ownerId',Integer,ForeignKey(archive.c.id),index=True),
            Column('content',Text,nullable=False),
            Column('attr',String(10),nullable=False,default=''),
            Column('type',String(16),nullable=False,default='comment'),
            Column('status',String(16),nullable=False,default='approved',index=True),
            Column('mail',String(200)),
            Column('url',String(200)),
            Column('ip',String(64)),
            Column('agent',String(200))
        )
mapper(Meta,meta)
mapper(User, user)
mapper(Relationship,relationship)
'''
mapper(Category,slug)
mapper(Tag,tag)
'''
mapper(Application,application)
mapper(Archive,archive)
mapper(Option,option)
mapper(Comment,comment)


_db_engine = None
session = None
from config import  db_dns , db_host , db_name ,db_passwd
if db_dns == 'sqlite':
    from sqlite3 import dbapi2 as sqlite
    from sqlalchemy import create_engine
    _db_engine = create_engine('sqlite:///%s' %(db_name), echo=True)
    session = scoped_session(sessionmaker(bind=_db_engine))

def add_comment():
    c1= Comment()
    c1.appid=1
    c1.parent=0
    c1.authorId=1
    c1.ownerId=2
    c1.content=u'这是一个测试评论哦！！'
    session.add(c1)
    session.commit()
    
def test_app():
    print session.query(Application).all()
def new_option():
    a =session.query(Application).one()
    o = Option(a,'pageCount','20')
    session.add(o)
    session.commit()
def query_option():
     a  = session.query(Application).one()
     print a.get_option('pageCount')
     a.set_option('test','test')
     session.commit()
def create_db():
    Base.metadata.create_all(_db_engine)

'''
u =User()
u.name='test1'
u.password='password'
u.mail='feiyd0000@gmail.com'
session = scoped_session(sessionmaker(bind=engine))
session.add(u)
session.commit()
print session.query(User).one().lastip
app = Application()
app.domain='127.0.0.1'
session.add(app)
session.commit()
_app= session.query(Application).one()
print _app.id ,_app.domain
'''
def create_tag():
    m  = Meta()
    m.name=u'工作'
    m.type='category'
    r  = Relationship()
    r.appId=1
    r.cid=1
    r.mid=3
    session.add(m)
    session.add(r)
    session.commit()
    
if __name__=='__main__':
    c1= Comment()
    c1.appid=1
    c1.parent=0
    c1.authorId=1
    c1.ownerId=2
    c1.content=u'这是一个测试评论哦！！'
    session.add(c1)
    session.commit()
     
    
     
    
