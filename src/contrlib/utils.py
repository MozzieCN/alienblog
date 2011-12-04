#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       utils.py
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
 

def  load_module(modname,filename):
    import sys
    import imp
    if modname in  sys.modules:
        return sys.modules[modname]
    m = imp.new_module(modname)
    m.__file__=filename
    try:
        execfile(m.__file__, m.__dict__)
    except IOError, e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return m
def  create_query_sql(db,cls,**kwords):
    sqlobj = db.query(cls)
    for key,value in kwords.iteritems():
        if hasattr(cls,key):
            if isinstance(value,(tuple,list)):
                sqlobj = sqlobj.filter(getattr(cls,key).in_(value))
            else:
                sqlobj = sqlobj.filter(getattr(cls,key)==value)
    return sqlobj
            
    
