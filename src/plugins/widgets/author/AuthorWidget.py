#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       plugins.widgets.author.AuthorWidget.py
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

class AuthorWidget(plugin.Widget):
    
    
    author_url='http://www.gravatar.com/avatar/%s?s=%d&amp;r=X&amp;d=%s'
           
    def __init__(self):
        plugin.Widget.__init__(self,'system.author.info')
    
    def parse(self,**kwords):
        mail = kwords.pop('mail')
        width = kwords.pop('width',32)
        height = kwords.pop('height',32)
        cls   = kwords.pop('avatar-class','avatar')
        if mail :
            #什么什么的运算
            pass
        mail = '98b58b690d0016861c6ee4c494f6677b'
        from alien.htmlwappers import Img,Div,tag,A
        img = Img(**{'class':cls})
        img.width=width
        img.height=height
        img.alt='default'
        img.src=self.author_url % (mail,width,'default-png')
        cls  = kwords.pop('author-info-class','fn')
        url  = kwords.pop('url','www.baidu.com')
        name = kwords.pop('name','呵呵')
        author_info=tag('cite',**{'class':cls})
        if not url:
            author_body = name
        else:
            author_body=A(body=name,
                          **{
                             'rel':'external nofollow',
                             'href':url
                            }
                          ).render()
        author_info.body=author_body
        return '%s\r\n%s'%(img.render(),author_info.render())
        