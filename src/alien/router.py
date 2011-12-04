#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       RouteRole.py
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
import re
import types
class Router(object):
    def __init__(self,role,syntax=None):
        self.syntax = re.compile(syntax) if syntax else re.compile(r'(?<!\\):([a-zA-Z_][a-zA-Z_0-9]*)?(?:#(.*?)#)?')
        self.role = role
        self._complie_pattern = None

    def match(self,path):
        if not self._complie_pattern :
            self._complie_pattern = self._complie(self.role)
        return self._complie_pattern.match(path)

    def apply(self,obj):
        print '------> role apply:',self.role,obj
        if hasattr(obj,'__dict__'):
            return self._apply(lambda x:getattr(obj,x))
        elif isinstance(obj,list):
            return self._apply(lambda x:obj.pop())
        elif isinstance(obj,tuple):
            return self.apply(list(obj))
        else:
            return self._apply(lambda x:obj)
            
    def _apply(self,func):
        out = u''
        for i ,part in enumerate(self.syntax.split(self.role)):
            if i%3 ==0:
                out += part
            if i%3 ==1:
                out += unicode(func(part))
        return out
       
    '''            
    def apply_obj(self,obj):
        return self.apply(self.role,obj.__dict__)
    def apply(self,path,dictobj):
        print 'role =-->' ,self.role
        out = u''
        for i ,part in enumerate(self.syntax.split(self.role)):
            print 'i,parg' , i, part
            if  i%3 ==0:
                out += part
            if  i%3 ==1:
                out +=unicode(dictobj[part])
        print 'out-.' ,out
        return out
    '''
    def match_dict(self):
        match = self.match(self.path)
        return [] if not match else match.groupdict()
            
    def _complie(self,role):
        out=r''
        for i, part in enumerate(self.syntax.split(role)):
            if i%3 == 0:   out += re.escape(part.replace('\\:',':'))
            elif i%3 == 1: out += '(?P<%s>' % part if part else '(?:'
            else:          out += '%s)' % (part or '[^/]+')
        return re.compile('^%s$'%out)

if  __name__ == '__main__':
    r=Router('/:filename#.*\.(png|js|css)#')
    print r.match('/aaaaa/static.css').groupdict()
