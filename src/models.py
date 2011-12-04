#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       models.py
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
class Relationship(object):
    pass
class Meta(object):
    pass
class Comment(object):
    pass
class Option(object):
    def __init__(self,app,key,value):
        self.appid = app.id
        self.key = key
        self.value = value
        
  
            
class Application(object):
    def __init__(self):
        self.domain = domain
        self.id = None

    def set_option(self,key,value):
        if '_options' not in self.__dict__:
            self.__dict__['_options'] = {}
        self._options[key] = value
        option = Option(self,key,value)
        self.options.append(option)
    def get_option(self,key,default=None):
        if '_options' not in  self.__dict__:
            self.__dict__['_options'] ={}
            for  option in self.options:
                self._options[option.key] = option.value
        v = self._options.get(key,None)
        return v  if v else default
class User(object):
    def __init__(self):
        self.id=None
        self.name=''
        self.password=''
        self.mail=''
        self.url=''
        self.displayName=''
        self.createdTime=None
        self.status='activated'
        self.group='visitor'
        self.authCode=''
        self.lastip=''
        self.lastlogin=None
    '''
    def __getattribute__(self, name):
        if name == 'password':
            pwd = object.__getattribute__(self, name)
            import base64
            print pwd , '---->'
            pwd = base64.b32decode(pwd) if pwd else ''
            print pwd , '<-----'
            return pwd
            
        else:
            return object.__getattribute__(self, name)
    '''
    def __setattr__(self, name, value):
        if name == 'password':
            import hashlib
            md5Util = hashlib.md5()
            md5Util.update(value)
            value = md5Util.hexdigest()
        object.__setattr__(self, name, value)

class Category(object):
    def __init__(self,name=''):
        self.id = None
        self.name=name
class Tag(object):
    def __init__(self,appId,archiveId,name):
        self.appId =appId
        self.archiveId=archiveId
        self.name =name
        self.click=0
class Archive(object):
    def __init__(self):
        self.id = None
        self.appid=''
        self.alias=''
        self.type='post'
        self.attr=''
        self.title=''
        self.desc=''
        self.content=''
        self.order=0
        self.author=''
        self.authorId=0
        self.status='publish'
        self.password=''
        self.allowComment=0
        self.parent=''
        self.category=None
        #self.pubTime=None
        #self.modifyTime=None
        self.commentCount=0
       # self.keywords=[]
        self.keywords=''
        self.click=0
        self.channel='website'
    '''
    @property
    def content(self):
        return self.content
    def get_id(self):
        return self.id
    def get_type(self):
        return self.type
    def get_status(self):
        return self.status
    def get_order(self):
        return self.order
    def get_author(self):
        return self.author
    def get_keywords(self):
        return self.keywords
    def need_password(self):
        return self.password is not ''
    '''
    
        
def main():
    return 0

if __name__ == '__main__':
	main()

