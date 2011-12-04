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
    def prepare(self):
        plugin.Extension.prepare(self)
        self.register('system.show.archives',self.show_archives)
        self.register('system.show.archive',self.show_archive)
        self.register('system.archives.count',self.get_archives_count)
    
    '''
    def register_actions(self):
        self.register_action('system.show.archives',self.show_archives)
        self.register_action('show.archive',self.show_archive)
    '''
    def _build_archives_sqlobj(self,**args):
        appid    = args.get('appid',None)
        status   = args.get('status',None)
        type     = args.get('type','post')
        status   = args.get('status','publish')
        channel  = args.get('channel','website')
        authorid = args.get('authorid',None)
        from models import Archive
        sqlobj = self.db.query(Archive)
        if appid: sqlobj = sqlobj.filter(Archive.appid==appid)
        if isinstance(type,(tuple,list)):
            sqlobj = sqlobj.filter(Archive.type.in_(type))
        else:
            sqlobj = sqlobj.filter(Archive.type==type)
        if authorid:
            sqlobj  = sqlobj.filter(Archive.authorId==authorid)
        if isinstance(status,(tuple,list)):
            sqlobj  = sqlobj.filter(Archive.status.in_(status))
        else:
            sqlobj  = sqlobj.filter(Archive.status==status)
        if isinstance(channel,(tuple,list)):
            sqlobj  = sqlobj.filter(Archive.channel.in_(channel))
        else:
            sqlobj  = sqlobj.filter(Archive.channel==channel)
        return sqlobj
    def get_archives_count(self,**args):
        sqlobj = self._build_archives_sqlobj()
        return sqlobj.count();
            
        

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
        sqlobj = self._build_archives_sqlobj()
        offset =  args.get('offset',None)
        limit  =  args.get('limit',None)
        if offset >0:
            sqlobj= sqlobj.offset(offset)
        if limit >0:
            sqlobj= sqlobj.limit(limit)
        return sqlobj.all()
        
        
        
        
        
        

def main():
	
	return 0

if __name__ == '__main__':
    import shcame
    a = ArchiveExtension()
    a.list_archive()
    

