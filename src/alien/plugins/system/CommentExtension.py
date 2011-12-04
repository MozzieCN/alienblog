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
    def register_actions(self):
        self.register_action('system.show.comments',self.show_comments)
    def show_comments(self,**kwords):
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
        print  'PPPPPPPPPPPPPPPP',parent
        sqlobj = sqlobj.filter(Comment.parent == parent)
        if int(limit) > 0 :
            sqlobj = sqlobj.offset(int(offset)).limit(limit)
        return sqlobj.all()

def main():
	
	return 0

if __name__ == '__main__':
	main()

