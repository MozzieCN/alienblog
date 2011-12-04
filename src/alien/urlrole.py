#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       urlrole.py
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


def BaseUrlRole(object):
    def  __init__(self,path):
        self.syntax = re.compile(r'(?<!\\):([a-zA-Z_][a-zA-Z_0-9]*)?(?:#(.*?)#)?')
        self.path = path
    def apply(self,*object):
        out = ''
        for i ,part in enumerate(syntax.split(rule)):
            if  i%3 ==0:
                out += part
            if  i%3 ==1:
                print part
                out +=_getattr__(object,part)
        return out

class t(object):
    def __init__(self):
        self.alias = 'alias1'
def main():
	bur = BaseUrlRole =('/:alias'):
    print bur.apply(t())
    
	return 0

if __name__ == '__main__':
	main()

