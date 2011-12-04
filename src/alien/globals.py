#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       globals.py
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

from functools import partial
from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase
from werkzeug.local import LocalStack, LocalProxy
DEFAULT_REQUEST_CLASS = RequestBase
DEFAULT_RESPONSE_CLASS= ResponseBase

__ALL__=[
            'ctx',
            'request',
            'response',
            'current_app',
            'environ',
            '_app_ctx_stack'
        ]
class AppContext(object):
    def __init__(self,
                  app,
                  environ,
                  session_key = None,
                  request_class=None,
                  response_class=None):
        self.app = app
        self.environ = environ
        self.request=None
        if  not request_class:
            request_class = DEFAULT_REQUEST_CLASS
        if  not response_class:
            response_class = DEFAULT_RESPONSE_CLASS
        self.request = request_class(environ)
        self.response= response_class()
        self.response.headers['Content-Type'] ='text/html'
        print request_class
        print self.request
    def push(self):
        top = _app_ctx_stack.top
        if top:
            top.pop()
        _app_ctx_stack.push(self)
    def pop(self):
        rv = _app_ctx_stack.pop()
        assert rv is self, 'Popped wrong request context.\ (%r instead of %r)'           % (rv, self)
    def __enter__(self):
         self.push()
    def __exit__(self,exc_type, exc_value, tb):
         self.pop()
    def __setattr__(self,name,value):
        self.__dict__[name] = value
def _lookup_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError('working outside of request context')
    return getattr(top, name)
_app_ctx_stack = LocalStack()
app_ctx_stack=_app_ctx_stack
ctx  = LocalProxy(partial(lambda:_app_ctx_stack.top))
current_app = LocalProxy(partial(_lookup_object, 'app'))
request = LocalProxy(partial(_lookup_object, 'request'))
response= LocalProxy(partial(_lookup_object,'response'))
session = LocalProxy(partial(_lookup_object, 'session'))
environ = LocalProxy(partial(_lookup_object,'environ'))
#g =LocalProxy(partial(_lookup_object, 'g'))

