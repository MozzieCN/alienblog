#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       alien.htmlwappers.py
#       
#       Copyright 2011  feiyd
#       
#       Created on 2011-11-28
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
import types
DEFAULT_IDS = {}
def  get_default_id(tagName):
    id = -1
    if tagName not in DEFAULT_IDS:
        id = 1
    DEFAULT_IDS[tagName] = '%s-%d' % (tagName, id)
    return  DEFAULT_IDS[tagName]
class BaseTag(object):
    KNOWS_ATTR = ['id','tagName','name','add_children','body','children']
    def  __init__(self, tagName,id=None,name=None, body=None, auto_id=False,id_func=None, **attrs):
        self._attrs = attrs
        self.tagName = tagName
        self.body = body
        self.id = id
        self.name=name
        self.children = []
        if not id and auto_id:
            id_func = id_func or attrs.pop('id_func', None) or get_default_id
            self.id =id_func
    def set_attr(self, attr, value):
        self._attrs[attr] = value
    def has_children(self):
        return len(self.children) > 0
    def render(self):
        if  not self.body and not self.has_children():
            attrs = self._prepare()
            return  u'<%s %s />' % (self.tagName, attrs)
        else:
            out = u''
            if self.has_children():
                out = u'\r\n'.join([c.render() for c in self.children])
            if self.body:
                out = self.body + out
            return  '<%s%s>%s</%s>' % (
                                      self.tagName,
                                      ' ' + self._prepare(),
                                      out,
                                      self.tagName
                                      )
    def update(self,attr,value):
        rv = self._attrs.pop(attr,None)
        if rv:
            if type(rv) == types.ListType:
                rv.extend(value)
            else:
                rv = list(rv,value)
        else:
            rv = value
        self._attrs[attr]=rv
            
    def _prepare(self):
        atts = []
        if self.id :
            self._attrs['id']=self.id
        if self.name:
            self._attrs['name']=self.name
        for  k , v  in  self._attrs.iteritems():
            if not  v :
                atts.append(k)
                continue
            elif type(v) == types.ListType  \
                or type(v) == types.TupleType:
                v = ' '.join(v)
            atts.append('%s="%s"' % (k, str(v)))
        return ' '.join(atts)
    def add_children(self, tag):
        self._check_children(tag)
        self.children.append(tag)
        return tag
    def _check_children(self, tag):
        if not isinstance(tag, BaseTag):
            raise TypeError('child must be BaseTag instance')
    def __setattr__(self, *args, **kwargs):
        key = args[0]
        if key in self.KNOWS_ATTR or key.startswith('_'):
            return object.__setattr__(self,*args,**kwargs)
        if key in ('class_','cls'):
            key = 'class'
        self._attrs[key] = args[1]
    '''
    def __setattr__(self, key, value):
       
        if key=='class_' or key =='cls':
            key = 'class'
        self._attrs[key] = value
    '''
    def __getattr__(self, key):
        if key not in self.__dict__:
            return self._attrs.get(key, None)
        return self.__dict__.get(key)

class Div(BaseTag):
    def __init__(self, **attrs):
        BaseTag.__init__(self, 'div', **attrs) 
class A(BaseTag):
    def __init__(self,href=None,body=None ,**attrs):
        attrs['href'] = href
        BaseTag.__init__(self, 'a',body=body, **attrs)
    def set_href(self, href):
        pass
class TagOl(BaseTag):
    def __init__(self, **attrs):
        BaseTag.__init__(self, 'ol', **attrs)
class TagLi(BaseTag):
    def __init__(self, **attrs):
        BaseTag.__init__(self, 'li', **attrs)    
class Span(BaseTag):
    def __init__(self,body,**atts):
        BaseTag.__init__(self,'span',body=body,**atts)
class Img(BaseTag):
    def __init__(self,*args,**kwords):
        BaseTag.__init__(self,'img',**kwords)
        
            
 
def  tag(tagName, **args):
    tagName = tagName.lower()
    if  tagName in __ALL_KNOWS_TAG__ or tagName.startswith('_'):
        return  __ALL_KNOWS_TAG__[tagName](**args)
    else:
        return BaseTag(tagName, **args)
        
                
 
        
__all__ =['Span','tag','A','Div','Img']
        
__ALL_KNOWS_TAG__ = {
                       'div':Div,
                       'ol' :TagOl,
                       'li' :TagLi,
                       'span':Span
                       }       
     
        
if __name__ == '__main__':
    div = BaseTag('div', **{'class':'comment'})
    a = BaseTag('a', **{'href':'www.baidu.com'})
    a.href = "www.google.com"
    div.add_children(a)
    tag('li',**{
                'ab':'a',
                'bc':'c'
                })
    print a.render()
    print div.render()
