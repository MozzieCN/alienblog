#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       framework.py
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
__all__=['get_instance']
__instance =None
from contrlib import  plugin
def get_instance(engine='bottle',workdir=None,plugindir='plugins',configdir=None):
    global __instance
    if not __instance:
        __instance = BottleFrameWork(workdir,plugindir,configdir) if engine=='bottle' else FrameWork
    return  __instance


    
class FrameWork:
    def  __init__(self,workdir=None,plugindir='plugins',configdir=None):
        if not workdir:
            import os
            workdir=os.getcwd()
        self.workdir=workdir
        if isinstance(plugindir,(tuple,list)):
            self.plugindir = ['%s/%s' % ( workdir,x) for x in plugindir]
        else:
            self.plugindir =  (plugindir)
        self._db_engine = None
        self.plugin_manager= plugin.PluginManager(self,self.plugindir)
        self.plugin_manager._load()
        
    def get_db(self):
        if not self._db_engine:
            from  shcema import session
            self._db_engine = session
        return self._db_engine
        '''
        if not self._db_engie:
            from config import  db_dns , db_host , db_name ,db_passwd
            if db_dns == 'sqlite':
                from sqlite3 import dbapi2 as sqlite
                from sqlalchemy import create_engine
                self._db_engine = create_engine('sqlite:///%s' %(self.get_cfg('database.db_name')), echo=True)
        return self._db_engine
        '''
   
        

    def find_widget(self,name):
        return self.plugin_manager.find_widget(name)

    def do_action(self,action,**args):
        try:
            result  = None
            for handler,sync in  self.plugin_manager.next_plugin_by_action(action):
                _status = None
                _presult = handler(__action__=action,__result__=result,**args)
                if isinstance(_presult,(tuple)):
                    _status , _result= tuple(_presult)
                elif isinstance(_presult,dict):
                    _status  = _presult.getkey('status',None)
                    _result  = _presult.getkey('result',None)
                else:
                    _result  = _presult
                if _result:
                    result = _result
                if _status == plugin.DONE:
                    break
            return result
        except:
            raise
        '''
        plugins = self.plugin_manager.find_plugins_by_action(action)
        print plugins
        if not plugins:
            return None
        else:
            
            for action,handler,order,sync in plugins:
                print action,handler,order,sync
                status , result  = handler(**args)
        '''
    def create_app(self,host):
        app =self._create_app(host)
        return AlienApp(host,app)
    @property
    def curr_app(self):
        environ = self.environ
        return environ['__alien_app__'] if '__alien_app__' in environ else None
    @property
    def environ(self):
        pass

    def _create_app(self,host):
        pass 
                
class AlienApp(object):
    def __init__(self,host,wapped_app):
        self.wapped_app  = wapped_app
        self.host  = host
        self.urls = []
        self._app = None
        self.archive_url_role=None
        self.category_url_role=None
        self.tag_url_role=None
        self._build_app()
    def route(self,urls):
        #self.urls.extend(urls)
        from alien import framework
        for path , method, func in  urls:
            framework.route(app=self,path=path,method=method,func=func)
    def _build_app(self):
        from alien import framework
        from models import Application
        import urlrole
        db = framework.get_db()
        self._app = db.query(Application).filter(Application.domain == self.host).one()
        self.archive_url_role = self._app.get_option('archive_url_role')
        if not self.archive_url_role:
            self.archive_url_role = urlrole.default_archive_role
        else:
            self.archive_url_role = urlrole.UrlRole(self.archive_url_role)
        self.category_url_role = self._app.get_option('category_url_role')
        if not self.category_url_role:
            self.category_url_role= urlrole.default_category_role
        else:
            self.category_url_role= urlrole.UrlRole(self.category_url_role)
        self.tag_url_role = self._app.get_option('tag_url_role')
        if not self.tag_url_role:
            self.tag_url_role = urlrole.default_tag_role
        else:
            self.tag_url_role = urlrole.UrlRole(self.tag_url_role)
    def __getattr__(self,key):
        if key not in  self.__dict__:
            return getattr(self._app,key)
    '''
    def __getitem__(self,key):
        print 'key==>' ,key
    '''
    def __call__(self, environ, start_response):
        print '______call__________'
        environ['__alien_app__'] = self
        return self.wapped_app(environ,start_response)
        

class BottleFrameWork(FrameWork):
    #rom bottle import Bottle,app,request,response
    def __init__(self,workdir=None,plugindir='plugins',configdir=None):
        FrameWork.__init__(self,workdir,plugindir,configdir)
    @property
    def environ(self):
        from bottle import request
        return request.environ
    def _create_app(self,host):
        from bottle import Bottle
        import bottle
        bottle.DEBUG=True
        app  = Bottle()
        return app
    def render(self,filename=None,**args):
        app  = self.curr_app
        from bottle import template,Jinja2Template
        apptheme = app.get_option('themeUrl')
        print 'apptheme ---->' ,apptheme
        apptheme = 'themes/mono'
       # themepath= '%s/%s' %('themes', apptheme if apptheme else 'default')
        localvars  = {
                        'Widget':self.find_widget,
                        'do_action':self.do_action,
                        '_option': app.get_option
                     }
        return template(
                        filename,{'path':'static'},
                        localvars,
                        template_adapter=Jinja2Template,
                        template_lookup=[apptheme],
                        **args
                     )
        
    def send_file(self,*arg ,**k):
        app  = self.curr_app
        apptheme = app.get_option('theme')
        themepath= '%s/%s' %('themes', apptheme if apptheme else 'default')
        from bottle import static_file
        import os
        return static_file(*arg,root=os.getcwd())
    def route(self,app=None,path=None,func= None ,method='GET'):
        #app.route(path,method,callback=func)
        from bottle import Bottle
        _app = None
        if not app:
            _app = self.curr_app.wapped_app
        elif isinstance(app,AlienApp):
            _app = app.wapped_app
        elif isinstance(app,Bottle):
            _app = app
        else:
            raise TypeError, 'app must instance Bottle or AlienApp '
        _app.route(path,method=method,callback=func)
        
            
        

