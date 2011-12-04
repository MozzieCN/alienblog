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
from alien import current_app,ctx,request,environ
from view_models import *
def new_comment(**kwords):
    archive = ctx.plugin_manager.do_action('system.show.archive',
                                 appid=current_app.id,
                                 **kwords
                                 )
    if not archive:
        pass
        #TODO 没有找到文档
    if archive.allowComment ==1:
        pass
        #TODO 不允许评论
    archive.commentCount +=1
    url = request.form.get('url',None)
    mail= request.form.get('mail',None)
    author=request.form.get('author',None)
    parentid=request.form.get('parent',None)
    text    =request.form.get('text',None)
    remote_addr = request.remote_addr
    user_agent  ='%s/%s' %( request.user_agent.platform,
                            request.user_agent.browser
                            )
    ctx.plugin_manager.do_action('system.new.comment',
                  author = author,
                  mail   = mail,
                  url    = url,
                  ownerId= archive.id,
                  parent=parentid,
                  content=text,
                  ip     =remote_addr,
                  agent  = user_agent
                  )
    return ctx.render('single',archive=WappedArchive(archive))
def index(page=1):
    page = int(page)
    page_count = current_app.get_option('pageCount') or 2
    totle_count = ctx.plugin_manager.do_action('system.archives.count',
                                               appid=current_app.id,
                                               status='post'
                                               )
    if totle_count and int(totle_count) >0:
        archives  = ctx.plugin_manager.do_action(
                            'system.show.archives',
                            offset = (page*page_count)-page_count,
                            appid=current_app.id,
                            limit = page_count
                            )
        if archives:
            return  ctx.render('index',archives=WappedPool(archives,WappedArchive),page=Page(totle_count,page,page_count,ctx.index_url_for))
    else:
        return ctx.render('index')
def show_tag(**kword):
    pass
def show_category(**keword):
    pass
def show_archive(**kwords):
    archive = ctx.plugin_manager.do_action('system.show.archive',
                                  appid=current_app.id,
                                  **kwords
                                  )
    if archive:
        return ctx.render('single',archive=WappedArchive(archive))
    return 'pk'

