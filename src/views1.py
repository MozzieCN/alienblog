#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       views.py
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
from  alien import framework
from  view_models import *
def index(page=1):
    print framework
    app  = framework.curr_app
    pageCount = app.get_option('pageCount')
    
    archives = framework.do_action('show.archives',
                                     page=page,
                                     appid=app.id,
                                     pageCount= pageCount if pageCount else 20
                                    )
    if archives:
        return framework.render('index',archives=ArchiveStock(archives),page=page)
    return framework.render('text',**{'name':'index'})

def show_archive(**kwords):
    app  = framework.curr_app
    archive = framework.do_action('show.archive',
                                  appid=app.id,
                                  **kwords
                                  )
    if archive:
        return framework.render('single',archive=WappedArchive(archive))
    return 'pk'
def static_files(path):
    print '===>',path
    return framework.send_file(path)
    
if __name__ =='__main__':
    print static_files('ssss')
