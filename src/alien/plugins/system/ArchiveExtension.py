#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       ArchiveExtension.py
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
from contrlib.plugin import DONE

class ArchiveExtension(plugin.Extension):
    
    def __init__(self):
        plugin.Extension.__init__(self,'ArchiveExtension')
    
        
    def register_actions(self):
        self.register_action('show.archives',self.show_archives)
        self.register_action('show.archive',self.show_archive)

    def show_archive(self,**args):
        appid    = args.get('appid',None)
        id       = args.get('id',None)
        alias    = args.get('alias',None)
        from models import Archive
        sqlobj = self.db.query(Archive)
        if appid:
            sqlobj = sqlobj.filter(Archive.appid==appid)
        if id:
            sqlobj = sqlobj.filter(Archive.id==id)
        if alias:
            sqlobj = sqlobj.filter(Archive.alias==alias)
        return sqlobj.one()
    def show_archives(self,**args):
        appid    = args.get('appid',None)
        type     = args.get('type','post')
        authorid = args.get('authorid',None)
        status   = args.get('status','publish')
        channel  = args.get('channel','website')
        page     = int(args.get('page',1))
        pageCount= int(args.get('pageCount',20))
        from models import Archive

        #db  = self.get_db()
        from shcema import session
        query = session.query(Archive)
        if appid:
            query  = query.filter(Archive.appid == appid)
        if isinstance(type,(tuple,list)):
            query  = query.filter(Archive.type.in_(type))
        else:
            query  = query.filter(Archive.type==type)
        if authorid:
            query  = query.filter(Archive.authorid==authorid)
        if isinstance(status,(tuple,list)):
            query  = query.filter(Archive.status.in_(status))
        else:
            query  = query.filter(Archive.status==status)
        if isinstance(channel,(tuple,list)):
            query  = query.filter(Archive.channel.in_(channel))
        else:
            query  = query.filter(Archive.channel==channel)
        count  = query.count()
        objects  =None
        if count > 0 :
            objects = query.offset((page*pageCount)-pageCount).limit(pageCount).all()
        print  'count,obj' , count ,objects
        return objects
        
        
        
        
        
        

def main():
	
	return 0

if __name__ == '__main__':
    import shcame
    a = ArchiveExtension()
    a.list_archive()
    

