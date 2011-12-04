# -*- coding: utf-8 -*-
#
#       deploy.py
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
#       MERCHANTABILITY or FITNESS FOdeployR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from threading import Lock
import time
from bottle import run
from datetime import datetime
import schema
import views
from functools import partial
from alien import ctx

from template import jinja2Template
class SubdomainDispatcher(object):
    def __init__(self, domain, create_app):
        self.domain = domain
        self.create_app = create_app
        self.lock = Lock()
        self.instances = {}
    def get_application(self, host):
        with self.lock:
            app = self.instances.get(host)
        if app is None:
            app = self.create_app(host)
            self.instances[host] = app
        return app
    def __call__(self, environ, start_response):
        host = environ['HTTP_HOST']
        host = host.split(':')[0]
        app = self.get_application(host)
        if not app :
            from alien.web_exceptions import BadRequest
            _badRequest = BadRequest()
            start_response('%d %s' % (int(_badRequest.code), _badRequest.status), _badRequest.header_list())
            return _badRequest.body
        return app(environ, start_response)
def create_app(domain):
    app = None
    from models import Application, Option
    try:
        app = schema.session.query(Application).filter(Application.domain == domain).one()
        app_options = schema.session.query(Option).filter(Option.appid == app.id).all()
        options = {}
        routes = {}
        map(lambda x:options.setdefault(x.key, x.value), app_options)
        from alien.app import Alien
        from alien import ctx
        aplien_app = Alien(domain, options=options)
        aplien_app.add_route('/', views.index)
        for  s in  default_route_funcs:
            router_role = options.pop('%s_router' % s, None)
            router = None
            if not router_role:
                router = default_routers.get('default_%s_router' % (s))
            else:
                from alien.router import Router
                router = Router(router_role)
            if router:
                aplien_app.add_route(router.role, default_route_funcs.get(s))
                options['__%s_url_for__' % s] = url_for(router)
        aplien_app.add_route('/:alias.html/comment',views.new_comment,'POST')
        aplien_app.add_route('/:filename#.*\.(png|js|css|gif)#', static_file)
        aplien_app.add_before_request(before_request)
        aplien_app.add_after_request(after_request)
        aplien_app.id = app.id
        
        return aplien_app
    except Exception , e:
        print '----', e
import os
def static_file(filename):
    from alien.app import send_file
    return send_file(filename, os.getcwd())
from alien.router import Router
default_routers = {
                'default_archive_router':Router('/:alias.html'),
                'default_category_router':Router('/categroy/:name/'),
                'default_tag_router':Router('/tag/:name/'),
                'default_index_router':Router('/page/:page/')
                 }
default_route_funcs = {
                    'index':    views.index,
                    'archive' : views.show_archive,
                    'category': views.show_category,
                    'tag':      views.show_tag
                 }
renders = {}
render_lock = Lock()

class url_for(object):
    def __init__(self,router):
        self._router = router
    def apply(self,obj):
        return '%s://%s%s'%(
                            ctx.environ['wsgi.url_scheme'],
                            ctx.environ['HTTP_HOST'],
                            self._router.apply(obj)
                            )
def register_js(id ,text):
    from alien import ctx
    if not hasattr(ctx,'__static__'):
        setattr(ctx,'__static__',{})
    id  = '%s-js' % id 
    if id in ctx.__static__: return 
    if text.find('.js') < 0:
        if not text.startswith('<script>'):
            text  = '<script>\r\n%s\r\n</script>' %text
    ctx.__static__[id] = text

def footer():
    from alien import ctx
    out = u''
    if hasattr(ctx,'__static__'):
        out = '\r\n'.join([x for x in ctx.__static__.values()])
    if hasattr(ctx,'__alien_request_start_time__') :
        t1 = (time.time()  - getattr(ctx,'__alien_request_start_time__'))
        out += str('<!-- expire time %f ms.-->'  %(t1 /1000))
    print 'ctx----->',out
    return out
        
def before_request():
    from alien import ctx, current_app, session
    for  s in  default_route_funcs:
        setattr(ctx,'%s_url_for' %s ,
                    current_app.options['__%s_url_for__' %s].apply)
    setattr(ctx, 'plugin_manager', pm)
    setattr(ctx, 'db', schema.session)
    template_engine = None
    with render_lock:
        template_engine = renders.get(current_app.name, None)
    if not template_engine:
        template_engine = jinja2Template(
                                    lookup=['themes/%s' % current_app.get_option('theme')],
                                    globals={
                                        'session':session,
                                        '_option':current_app.get_option,
                                        'Widget':pm.find_widget,
                                        '_footer':footer
                                    })
    renders[current_app.name] = template_engine
    setattr(ctx, 'render', template_engine.render)
    setattr(ctx,'_js',register_js)
    setattr(ctx,'__alien_request_start_time__',time.time())

def after_request():
    from alien import ctx
    setattr(ctx,'__alien_request_end_time__',datetime.now())
import config
theme_path = 'themes'
if hasattr(config, 'theme_path'):
    theme_path = config.theme_path
from contrlib.managers import ThemeManager, PluginManager
import os
tm = ThemeManager(os.getcwd() + '/' + theme_path)
tm._load_themes()
pm = PluginManager('plugins')
app = SubdomainDispatcher('example', create_app)
run(app, host='localhost', port=8080)

def main():
    return 0

if __name__ == '__main__':
	main()

