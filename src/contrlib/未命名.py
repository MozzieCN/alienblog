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

from alien import current_app,ctx
from view_models import *
def index(page=1):
    pageCount = current_app.get_option('pageCount') or 20
    archives  = ctx.plugin_manager.do_action(
                        'system.show.archives',
                        page=page,
                        appid=current_app.id
                        pageCount = pageCount
                )
    if archives:
        return  ctx.render('index',archives=ArchiveStock(archives),page=page)
    return ctx.render('text',**{'name':'index'})
    

