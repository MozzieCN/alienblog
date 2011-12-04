#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       exceptiones.py
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
from httplib import responses as HTTP_CODES
from urllib import quote

class HttpException(Exception):
    def __init__(self,code,message=None,headers={'Content-Type':'text/html'}):
        self._code = code
        self._message = message
        self._headers= headers
        self.headers['Content-Length'] = str(len(self.body))
        Exception.__init__(self,'%d %s' % (int(self.code),self.status))
    
    @property
    def headers(self):
        return self._headers
    @property
    def status(self):
        return HTTP_CODES[self.code]
    @property
    def code(self):
        return self._code
    @property
    def body(self):
           return (
             '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
             '<title>%(code)s %(name)s</title>\n'
             '<h1>%(name)s</h1>\n'
             '%(description)s\n'
         ) % {
            'code':         self.code,
            'name':         self.status,
            'description':  self.message
        }
    def header_list(self):
        return [(key,value) for key,value in self.headers.iteritems()]

class BadRequest(HttpException):
        message ='<p>The browser (or proxy) sent a request that this ' \
         'server could  not understand.</p>'
        def __init__(self):
            HttpException.__init__(self,400,message=self.message)
            
class MethodNotAllowed(HttpException):
    def __init__(self,valid_methods,message=None):
        HttpException.__init__(self,405,message)
        if valid_methods:
            self.headers.update({'Allow':', '.join(valid_methods)})
class NotFound(HttpException):
    message = 'The Page Not Found'
    def __init__(self,message=None):
        HttpException.__init__(self,404, message or self.message)

class InternalServerError(HttpException):
    message = 'Internal Server Error : %s \\r\\n  sys_info: \\r\\n %s' 
    def __init__(self,exception,sys_info):
        HttpException.__init__(self,500,self.message %(exception.message,sys_info))
