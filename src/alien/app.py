#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       app.py
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
from  globals import _app_ctx_stack,AppContext
from  url_adapter import RouteException ,NoSuchRoute
from  web_exceptions import *
from  httplib import responses as  http_codes
def makelist(data):
    if isinstance(data, (tuple, list, set, dict)): return list(data)
    elif data: return [data]
    else: return []

class Alien(object):
    def __init__(self,name=None,
                      static_path=None,
                      url_adapter=None,
                      request_class=None,
                      response_class=None,
                      session_key  = None,
                      options={}):
        self.name   = name
        self.static_path=static_path
        self.options = options
        self.before_request_funcs =[]
        self.after_request_funcs=[]
        self.routes=[]
        self.request_class= request_class
        self.error_handlers = {}
        if not url_adapter :
            from  url_adapter import default_adpater
            self.url_adapter = default_adpater
        self.response_class = response_class
        self._options=options
    def create_context(self,environ):
        return AppContext(self,environ,self.url_adapter,self.request_class)

    def add_route(self,path,view_func=None,method='GET',**options):
        method = makelist(method)
        for m in method:
            m = m.upper()
            cfg = dict(path=path,
                       method=m,
                       view_func=view_func,
                       app=self,
                       options=options
                        )
            #cfg[id]= self.routes
        self.routes.append(view_func)
        self.url_adapter.add_url(path=path,method=m,target=view_func)
    def get_option(self,key):
        return self.options.get(key,None)
 #   def add_url(self,path=None,method='GET',view_func=None,**options):
    def context(self):
        return _app_ctx_stack.top
    def add_before_request(self,func):
        assert func and callable(func) , 'func must be a callable'
        self.before_request_funcs.append(func)
    def add_after_request(self,func):
        assert func and callable(func) , 'func must be a callable'
        self.after_request_funcs.append(func)
    def _before_request(self):
        for func in self.before_request_funcs:
            func()
    def _after_request(self):
        for func in self.after_request_funcs:
            func()
    def set_error_handler(self,code,func):
        assert func and callable(func) , 'func must be a callabe'
        self.error_handlers[code] = func
    def _handle_http_error(self,code):
        print  code
        handler = self.error_handlers.get(code,None)
        if  handler:
            return handler()
    def _match(self,environ):
        try:
            handle,args = self.url_adapter.match(environ)
            environ['route.handle'] = handle 
            environ['route.url_args'] = args
            return handle,args
        except RouteException , e:
            raise
            
    def _handle(self,appctx):
        func ,args = self._match(appctx.environ)
        try:
            return func(**args)
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception ,e:
            print  '================>',e
            import sys,traceback
            print sys.exc_info()
            traceback.print_exc()
            raise InternalServerError(e,'as')
        
    def dispatch(self):
        req = _app_ctx_stack.top.request
        environ = _app_ctx_stack.top.environ
        self._before_request()
        rv = None
        try:
            rv = self._handle(_app_ctx_stack.top)
            self._after_request()
        except HttpException ,he:
            raise
        return rv

    def _cast(self,rv,request,response):
        if not rv:
            print 'rv'
    def _cast_response(self,rv,req,res):
        if not rv:
            res.headers['Content-Length'] = 0
            rv = []
        if isinstance(rv,(unicode)):
            rv = rv.encode(res.charset)
        if isinstance(rv, bytes):
            res.headers['Content-Length'] = str(len(rv))
            
            rv = [rv]
        if isinstance(rv,HttpException):
            out = self._handle_http_error(rv.code)
            res = rv
            out = out or res.body
            return  self._cast_response(out,req,res)
        code,status = self._parse_status(res)
        try:
            if not code :
                raise InternalServerError()
            if not status:
                raise HttpException(code)
        except:
            return self._cast_response(out,req,res)
        header_items= self._parse_headers(res)
        print 'header_items ,res' ,header_items,res
        return code,status,header_items,rv

    def _parse_status(self,res):
        out = None
        for  rv in ('code','status_code','status'):
            if hasattr(res,rv):
                out =  getattr(res,rv)
                break;
        if out:
            if isinstance(out,str):
                    if out.isdigit():
                        return  int(out),http_codes[out]
                    else:
                        return out.split(' ')
            if isinstance(out,int):
                    return  out,http_codes[out]
            if isinstance(out,(tuple,list)):
                    return out
    def _parse_headers(self,res):
        try:
            headers = getattr(res,'headers')
            return [(k,str(v)) for k,v in headers.iteritems()]
        except AttributeError :
            out =None
            for  attr in  ('header_list','headerlist'):
                if hasattr(res,attr):
                    return getattr(res,attr)
                    
    def __call__(self,environ, start_response):
        environ['__alien.app__'] = self
        with(self.create_context(environ)):
            rv = None
            req = _app_ctx_stack.top.request
            res = _app_ctx_stack.top.response
            try:
                rv  =  self.dispatch()
            except  (KeyboardInterrupt, SystemExit, MemoryError):
                raise
            except HttpException ,e:
                rv  = e
            import globals
            req = globals.app_ctx_stack.top.request
            print globals.app_ctx_stack.top
            print dir(globals.app_ctx_stack.top)
            code,status,header_items,out = self._cast_response(rv,req,res)
            # rfc2616 section 4.3
            
            if code in (100, 101, 204, 304) or req.method == 'HEAD':
                out = []
            
            start_response('%d %s' %(int(code),status),header_items)
            return out
    def __getattr__(self,key):
        if key not in self.__dict__:
            return self.options.get(key,None)
        return self.__dict__.get(key)

def q404():
    print '404'
    #return '40asdfasdfwerwerweoroweorwoeoweowe4'
def bq():
    print 'before request'
def index(path):
    print path
def start_response(status_code,header_items):
    print status_code,header_items
if __name__ == '__main__':
    app = Alien('text')
    app.add_before_request(bq)
    app.set_error_handler(404,q404)
    app.add_route('/:path.html',view_func=index)
    d = {'PATH_INFO':'/xxxxxxx.html','REQUEST_METHOD':'POST'}
    print app(d,start_response)
    



def send_file(filename,root,mimetype='auto'):
    import os
    root = os.path.abspath(root) + os.sep
    filename = os.path.abspath(os.path.join(root, filename.strip('/\\')))
    print filename
    if not filename.startswith(root):
        raise '403'
    if not os.path.exists(filename):
        raise '404'
    if not os.access(filename,os.R_OK):
        raise '403'
    res = _app_ctx_stack.top.response
    stats = os.stat(filename)
    res.headers['Content-Length']=stats.st_size
    import time
    lm = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(stats.st_mtime))
    res.headers['Last-Modified']=lm
    import mimetypes
    mimetype = mimetypes.guess_type(filename)
    if mimetype:
        res.headers['Content-Type']=mimetype
    else:
        res.headers['Content-Type']='text/plain'
    #TODO 304
    with open(filename,'rb') as f:
        return  f.read()
