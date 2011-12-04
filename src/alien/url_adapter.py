#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       url_adapter.py
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
from router import Router
class RouteException(Exception):
    pass
from web_exceptions import *
NoSuchRoute=RouteException('Not Such Route')
class BaseUrlAdapter(object):
    def __init__(self):
        self.routes = {}
        self.routers ={}
    def add_url(self,path,method,target,name=None):
        if path in self.routes:
            self.routes[path][method.upper()] = target
        else:
            self.routes[path]={method.upper():target}
        if path not in self.routers:
            self.routers[path] = Router(path)
    def match(self,environ):
        pass
        
class AilenUrlAdapter(BaseUrlAdapter):
    def __init__(self,syntax=None):
        BaseUrlAdapter.__init__(self)
        self._router = Router(syntax)

    def _match_path(self,environ):
        match =None
        path = environ['PATH_INFO'] or '/'
        for rule,router in self.routers.iteritems():
            if path.count(':') < path.count('\\:'): continue
            match  = router.match(path)
            if match :return self.routes[rule],match.groupdict()
        return None , ()
    def match(self,environ):
        targets , args  =  self._match_path(environ)
        if not targets:
            raise NotFound
        method = environ['REQUEST_METHOD'].upper()
        if method in targets:
            return targets[method],args
        if method == 'HEAD' and 'GET' in targets:
            return targets['GET'],args
        if 'ANY' in targets:
            return targets['ANY'],args
        raise MethodNotAllowed(targets.keys())

default_adpater = AilenUrlAdapter()
        
        
        
           



if __name__ == '__main__':
	main()

