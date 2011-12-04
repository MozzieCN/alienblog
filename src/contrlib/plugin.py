#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       plugin.py
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
from utils import load_module
import os
class Plugin(object):
    def get_name(self):
        pass
    def __init__(self,name=None):
        self._manager  = None
        self.framework = None
        self.is_active = False
        self.name = name
    def get_name(self):
        return self.name
    def get_author(self):
        pass
    def get_desc(self):
        pass
    def actived(self):
        return self.is_active
    def active(self,manager):
        self._manager=manager
        self.is_active=True
    @property
    def db(self):
        if self._manager:
            return self._manager.get_db()
    def prepare(self):
        pass
   
class Extension(Plugin):
   
    def __init__(self,name):
        Plugin.__init__(self,name)
    def register(self,action,handler,order=3,sync=True):
        self._manager.register_action(action,handler,order,sync)

    def action_handler(self,action,order=3,sync=True):
        pass
            
    def register_actions(self):
        pass
    def register_action(self,action,handler,order=3,sync=True):
        manager = self.framework.plugin_manager
        manager.register_action(action,handler,order,sync)
        
class Widget(Plugin):
    def __init__(self,name):
        Plugin.__init__(self,name)
    def get_render():
        pass
    def do(self,**kwords):
        pass
    def get(self,**kwords):
        return self.do(**kwords)
class MissingWidget(Widget):
    def __init__(self,name):
        self.name = name
    def get_name(self):
        return 'Missing widget : %s' % self.name
    def do(self,**kwords):
        return self.get_name()

class test :
    def __init__(self,order):
        self.order=order
def main():
    tl=[test(2),test(1),test(1)]
    t2=[test(3),test(4)]
    print tl
   # print t2
    tl.sort(lambda x,y : 1 if x.order>y.order else -1)
  #  t2.sort(lambda x,y : 1 if x.order>y.order elif y>x -1 else 0)
    print tl
   # print t2
    return 0

if __name__ == '__main__':
	main()

DONE = 'done'
CONTINUE = 'continue'
