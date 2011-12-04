#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       CategoryExtension.py
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
from contrlib import plugin

class CategoryExtension(plugin.Extension):
    
    def __init__(self):
        plugin.Extension.__init__(self,'CategoryExtension')

    
    def prepare(self):
        plugin.Extension.prepare(self)
        self.register('system.show.categories',self.show_categories)
        
    def register_actions(self):
        self.register_action('system.show.categories',self.show_categories)

    def show_categories(self,**args):
        appid   = args.get('appid',None)
        from models import Category
        sqlobj = self.db.query(Category)
        if(appid):
            sqlobj = sqlobj.filter(Category.appid==appid)
        return sqlobj.all()

    
        
        
        

def main():
	
	return 0

if __name__ == '__main__':
    import shcame
    a = ArchiveExtension()
    a.list_archive()
    

