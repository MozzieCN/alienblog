#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       template.py
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
class BaseTemplate(object):
    extentions = ['tpl','html','thtml','stpl']
    def  __init__(self,lookup=[],encoding='utf-8',**kwrods):
        self.lookup = lookup
        self.encoding = encoding
    @classmethod
    def _search(cls,name,lookup):
        import os
        if os.path.isfile(name) : return name
        for fpath  in lookup:
            fname =  os.path.join(fpath,name)
            if os.path.isfile(fname) :return fname
            for ext in cls.extentions:
                if os.path.isfile('%s.%s'%(fname,ext)):
                    return '%s.%s' %(fname,ext)
    def render(name,**kwords):
        raise NotImplementedError
class jinja2Template(BaseTemplate):
    def __init__(self,lookup=[],**kwords):
        BaseTemplate.__init__(self,lookup,**kwords)
        extensions = kwords.pop('extensions', [])
        globals = kwords.pop('globals', {})
        from jinja2 import Environment,FunctionLoader
        self._lookup = Environment(loader=FunctionLoader(self._loader),extensions=extensions)
        self._lookup.globals.update(globals)
    def render(self,name, **kwords):
        tpl = self._lookup.get_template(name)
        print 'tpl->',tpl
        return tpl.render(**kwords)

    def _loader(self,name):
        fname = self._search(name,self.lookup)
        if fname:
            with open(fname,'rb') as f:
                return  f.read().decode(self.encoding)
        



def main():
	
	return 0

if __name__ == '__main__':
    jj = jinja2Template(lookup=['themes/default'])
    print jj.render('text',name1='n1')

