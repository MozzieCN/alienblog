#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       managers.py
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

class Theme(object):
    def __init__(self,name,path):
        self.name = name
        self.path = path
class ThemeManager(object):
    def __init__(self,theme_path):
        self.path = theme_path
        self.themes = {}

    def _load_themes(self):
        import os
        print self.path
        if not  os.path.exists(self.path):
            raise RuntimeError('Themes path  %s is  not  exists' %(self.path))
        if not  os.path.isdir(self.path):
            raise RuntimeError('Themes path  %s is  must be a  dir' % self.path)
        for  top, folders,files  in os.walk(self.path):
            if top == self.path:
                for  folder in folders:
                    self.themes[folder] = Theme(folder,'%s/%s' %(top,folder))

class PluginManager(object):
    def  __init__(self,path):
        self.path=path
        self.widgets={}
        self.actions={}
        self._load_from_path(self.path)
        
    def _load_from_path(self,path):
        import os
        from contrlib.utils import load_module
        if not  os.path.exists(path):
            print  'Plugin path  %s is  not  exists' %(path)
            exit(0)
        if not  os.path.isdir(path):
            print  'Plugin path  %s is  must be a  dir' % path
        for  top, folders,files  in os.walk(path):
            print top,folders,files
            for  f  in [x for x in files if  x.endswith('py') and not x=='__init__py']:
                print f
                try:
                    d =load_module(f[:-3],os.path.join(top,f))
                except IOError, e:
                    e.strerror = 'Unable to load configuration file (%s)' % e.strerror
                from contrlib.plugin import Widget,Extension
                for  member  in  dir(d):
                    _call = getattr(d,member)
                    if callable(_call) and hasattr(_call,'__class__'):
                        print _call
                        _plugin = _call()
                        if isinstance(_plugin,(Widget,Extension)):
                            if not _plugin.actived():
                                self._active_plugin(_plugin)
                            if isinstance(_plugin,Widget):
                                self._to_add_widget(_plugin)
                            elif isinstance(_plugin,Extension):
                                self._to_add_extendsion(_plugin)
                        else:
                            del  _plugin
            '''
            for f in  folders:
                self._load_from_path(os.path.join(top,f))
            '''
    def get_db(self):
        from  alien import ctx
        return ctx.db
    def _active_plugin(self,plugin):
        plugin.active(self)
        plugin.prepare()
    def _to_add_extendsion(self,extendsion):
        ename = extendsion.get_name() or extendsion.__name__
        #extendsion.register_actions()
        
        
    def _to_add_widget(self,widget):
        wname = widget.get_name() or widget.__class__
        self.widgets[wname]=widget
        self.widgets[wname].__manager__=self
    def register_action(self,action,handler,order,sync):
        '''
        import threading
        class handler_wapper(threading.Thread):
            def __init__(self,action,handler):
                threading.__init__(self,'Wapp Action %s Handler %s'%(action,handler))
        '''
            
        func = {'action':action,'handler':handler,'order':order,'sync':sync}
        action_func = []
        if action in self.actions:
            action_func=self.actions.pop[action]
        action_func.append(func)
        if len(action_func) >=1:
            action_func.sort(lambda x,y: 1 if int(x.order)>int(y.order) else -1)
        self.actions[action]=action_func
    def find_plugins_by_action(self,action):
        if action in self.actions:
            return self.actions[action]
    def do_action(self,action,**args):
        result  = None
        for handler,sync in self.next_plugin_by_action(action):
            out = handler(__action__=action,__result__=result,**args)
            if isinstance(out,(tuple)):
                _status , _result= tuple(out)
            elif isinstance(out,dict):
                _status  = out.getkey('status',None)
                _result  = out.getkey('result',None)
            else:
                _result  = out
            if _result:
                result = _result
            '''
            if _status == plugin.DONE:
                break
            '''
        return result
    def next_plugin_by_action(self,action):
        if action in self.actions:
            _plugins = self.actions[action]
            for p in _plugins:
                yield (p['handler'],p['sync'])
    def find_widget(self,name,**kwords):
        class wapper(object):
            def __init__(self,widget,**kwords):
                self._widget = widget
                self._kwords = kwords
            def get(self):
                return self._widget.do(**self._kwords)
            def parse(self):
                return self._widget.parse(**self._kwords)
        if name:
            value= self.widgets.get(name,None)
        if not value:
            value=MissingWidget(name)
        return wapper(value,**kwords)
    def _load(self):
        path = self.path
        if isinstance(path,(list,tuple)):
            print 'list'
            for  p  in path:
                self._load_from_path(p)
        else:
            self._load_from_path(path)
 
def main():
	
	return 0

if __name__ == '__main__':
	main()

