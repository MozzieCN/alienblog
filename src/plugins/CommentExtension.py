#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       CommentExtensiion.py
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
class CommentExtension(plugin.Extension):
    def __init__(self):
        plugin.Extension.__init__(self,'CommentExtension')
    def prepare(self):
        plugin.Extension.prepare(self)
        self.register('system.show.comments',self.show_comments)
        self.register('system.comments.count',self.get_coments_count)
        self.register('system.new.comment',self.new_comment)

    def _build_update_sql(self,obj=None,**args):
        if not obj:
            from models import Comment
            obj = Comment()
        for key,value in args.iteritems():
            setattr(obj,key,value)
        return obj
    def new_comment(self,**args):
        obj = self._build_update_sql(**args)
        self.db.add(obj)
        self.db.commit()
    def _build_sql_obj(self,**kwords):
        from models import Comment
        sqlobj = self.db.query(Comment)
        for key,value in kwords.iteritems():
            if hasattr(Comment,key):
                if isinstance(value,(tuple,list)):
                    sqlobj = sqlobj.filter(getattr(Comment,key).in_(value))
                else:
                    sqlobj = sqlobj.filter(getattr(Comment,key)==value)
        return sqlobj
            
    def get_coments_count(self,**kwords):
        sqlobj = self._build_sql_obj(**kwords)
        return sqlobj.count()
    def show_comments(self,**kwords):
        sqlobj = self._build_sql_obj(**kwords)
        offset = kwords.get('offset',0)
        limit  = kwords.get('limit',None)
        if limit:
            sqlobj =sqlobj.offset(offset).limit(limit)
        '''
        appid    = kwords.get('appid',None)
        id       = kwords.get('id',None)
        status   = kwords.get('status',None)
        parent   = kwords.get('parent',0)
        offset   = kwords.get('offset',0)
        limit    = kwords.get('limit',0)
        ownerId  = kwords.get('ownerId',None)
        from  models import Comment
        sqlobj   = self.db.query(Comment)
        if  id:
            sqlobj = sqlobj.filter(Comment.id == id)
        if  appid:
            sqlobj = sqlobj.filter(Comment.appid == appid)
        if ownerId:
            sqlobj = sqlobj.filter(Comment.ownerId== ownerId)
        if  status:
            import types
            if status == types.TupleType or status == types.ListType:
                sqlobj = sqlobj.filter(Comment.status.in_(status))
            else:
                sqlobj = sqlobj.filter(Comment.status == status)
        sqlobj = sqlobj.filter(Comment.parent == parent)
        if int(limit) > 0 :
            sqlobj = sqlobj.offset(int(offset)).limit(limit)
        '''
        return sqlobj.all()

def main():
	
	return 0

if __name__ == '__main__':
	main()

