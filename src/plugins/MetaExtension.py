#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       plugins.widgets.MetaExtension.py
#       
#       Copyright 2011  feiyd
#       
#       Created on 2011-11-25
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
#   
from contrlib import plugin
from contrlib.plugin import DONE

class MetaExtension(plugin.Extension):
    '''
    classdocs
    '''


    def __init__(self):
        plugin.Extension.__init__(self,'MetaExtendsion')
    
    def prepare(self):
        plugin.Extension.prepare(self)
        self.register('system.show.metas',self.show_metas)

    def show_metas(self,**kwords):
        from contrlib.utils import create_query_sql
        from models import Relationship,Meta
        '''
        sqlobj = create_query_sql(self.db,Relationship,**kwords)
        sqlobj =sqlobj.join(Meta) \
            .filter(Meta.id==Relationship.mid).filter(Meta.type==kwords.get('type'))
        #sqlobj = create_query_sql(self.db,Relationship,**kwords).join(Meta.id==Relationship.mid);'''
        appid = kwords.get('appId',None)
        type  = kwords.get('type',None)
        cid   = kwords.get('cid',None)
        sqlobj = self.db.query(Meta)
        if appid :
            sqlobj =sqlobj.filter(Relationship.appId==appid)
        if cid:
            sqlobj =sqlobj.filter(Relationship.cid == cid)
        if type:
            sqlobj =sqlobj.filter(Meta.type==type)
        sqlobj =sqlobj.filter(Relationship.mid == Meta.id)
        metas = sqlobj.all()
        return metas;
        