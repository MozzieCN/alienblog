#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       alien.py
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

from threading import Lock
from bottle import Bottle, run
app1=Bottle()
app2=Bottle()
class SubdomainDispatcher(Bottle):
    def __init__(self, domain, create_app):
        Bottle.__init__(self)
        self.domain = domain
        self.lock = Lock()
        self.instances = {}
    def get_application(self, host):
        with self.lock:
            app = self.instances.get(host)
        if app is None:
            app = self.create_app(host)
            self.instances[host] = app
        return app
    def create_app(self,domain):
        app=Bottle(domain)
        #app.routes=self.routes
        #app.router=self.router
        app.route('/')
        app.mount(app1,'/index')
        app.mount(app2,'/admin')
        print  "=>",domain
        if domain=='localhost:8080':
            app.config['ttttt']='111111111111'
        if domain=='127.0.0.1:8080':
            app.config['ttttt']='22222'
        return app
    def __call__(self, environ, start_response):
        host= environ['HTTP_HOST']
        host = host.split(':')[0]
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)
app= SubdomainDispatcher('example',None)
#app=Bottle()

@app2.route('/')
def hee():
    return 'heeee'
@app1.route('/')
def  he():
    from bottle import request
    app  = request.environ['bottle.app']
    print app.config['ttttt']
    return 'he'

run(app, host='localhost', port=8080)

def main():
    return 0

if __name__ == '__main__':
	main()

