# -*- coding: utf-8 -*-
#
#       view_models.py
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
from alien import ctx, current_app
from alien.htmlwappers import *
class WappedComment(object):
    def __init__(self, comment):
        self._comment = comment
        self._childrens = None
    def the_id(self):
        return self._comment.id

    def _get_childrens(self):
        self._childrens = ctx.plugin_manager.do_action(
                                'system.show.comments',
                                appid=self._comment.appid,
                                parent=self._comment.id,
                                status='approved',
                                ownerId=self._comment.ownerId
                                )
        
    def have_children(self):
        if self._childrens:
            return True
        self._get_childrens()
        return self._childrens and len(self._childrens) > 0
    def childrens(self):
        if self.have_children():
            for  children in self._childrens:
                yield  WappedComment(children)
    def the_content(self):
        return self._comment.content
    def the_time(self, format='%Y/%m/%d %H:%M:%S'):
        return self._comment.created.strftime(format)
    def the_email(self):
        return self._comment.mail
    def date(self):
        return self._comment.created
    def the_author(self):
        if self.the_url():
          return '<a href="%s" rel="external nofollow">Author</a>' \
                % (self.the_url())
        else:
            return 'Author'
    def the_url(self):
        return self._comment.url
class WappedCategory(object):
    def __init__(self, category):
        self._category = category
    def permalink(self):
        return ctx.category_url_for(self._category)
    def name(self):
        return self._category.name
    def displayName(self):
        return self._category.displayName
class WappedMeta(object):
    def __init__(self, meta, **args):
        self._meta = meta
        self._url_for = args.get('url_for', None)
    def the_permalink(self):
        return self.the_name \
            if not self._url_for else self._url_for(self._meta) 
    def the_name(self):
        return self._meta.name
class WappedArchive(object):
    def __init__(self, archive, stock=None):
        self.stock = stock
        self._archive = archive
        self._permalink = None
        self._tags = None
        self._category=None
    def the_id(self):
        return self._archive.id
    def the_permalink(self):
        if not self._permalink:
             self._permalink = ctx.archive_url_for(self._archive)
        return self._permalink
    def allowComment(self):
        return True if self._archive.allowComment == '0' else False
    def have_comments(self):
        return True if self._archive.commentCount > 0 else False
    def the_comments(self, page=None):
        page = page or 1
        itmes  = None
        page   = None
        args = {
                  'appid':current_app.id,
                  'parent':0,
                  'status':'approved',
                  'ownerId':self.the_id()
                  }
        count = ctx.plugin_manager.do_action('system.comments.count', **args)
        if count <= 0:
           items  = []
        else:
            page = Page(count,page,1)
            items = ctx.plugin_manager.do_action('system.show.comments', 
                                                    offset=page.curr_offset(),
                                                    limit=page.limit(),**args)
        return  WappedPool(items,WappedComment,style_template_class=CommentStyleTemplate),page
            
    def the_title(self):
        return self._archive.title
    def the_content(self):
        return self._archive.content
    def the_category(self):
        #return WappedCategory(self._archive.category)
        if not self._category:
            metas = ctx.plugin_manager.do_action('system.show.metas',
                                                 appId=current_app.id,
                                                 cid=self.the_id(),
                                                 type='category'
                                                 )
        if metas:
            self._category=WappedPool(metas,
                                      WappedMeta,
                                      **{
                                            'url_for':
                                            ctx.category_url_for
                                         }
                                      )
        return self._category
    def the_click(self):
        return self._archive.click
    def the_comment_url(self):
        return '%s/comment' % self.the_permalink()
    def category_popup_link(self, deli,default=None):
        category = self.the_category()
        if category:
            return category.list_items(parent=None,
                                       container=None,
                                       deli=deli
                                       )
        else:
            return default;
    def the_tags(self):
        if not self._tags:
            metas = ctx.plugin_manager.do_action('system.show.metas',
                                     appId=current_app.id,
                                     cid=self.the_id(),
                                     type='tag'
                                     )
            if metas:
                self._tags = WappedPool(metas, WappedMeta,
                                    **{
                                       'url_for':
                                       ctx.tag_url_for
                                       })
            else:
                self._tags = None
        return self._tags;
    def tags_popup_link(self, deli=None, default=''):
        deli = deli or u''
        tags = self.the_tags()
        if tags:
        	return tags.list_items(parent=None,container=None,deli=deli)
        else:
        	return default;
    def comments_popup_link(self, zero=None, one=None, more=None, title=None, comment_div=None):
        if not title:
            title = u'<<%s>>的评论'
        if title.find('%s') >= 0: title = title % self.the_title()
        if not comment_div:
            comment_div = u'comments'
        href = '%s#%s' % (self.the_permalink(), comment_div)
        return u'<a href="%s" title="%s">%s</a>' % (href, title, self.commentNums(zero, one, more))
    def commentNums(self, zero=None, one=None, more=None):
        count = self._archive.commentCount
        if count == 0:return zero
        if count == 1:return one
        else:
            if more:
                return more % (count) if more.find('%d') >= 0 else more
            return count
    def the_year(self):
        return self._archive.year
    def the_month(self):
        return self._archive.month
    def the_day(self):
        return self._archive.day
    def the_time(self, format='%Y/%m/%d %H:%M:%S'):
        return self._archive.pubTime.strftime(format)


    
class WappedPool(object):
    def __init__(self,
                 iterable,
                 wapped_class,
                 style_template_class=None,
                  **wapped_args):
        self._iterable = iterable
        self._index = 0
        self._length = len(self._iterable)
        self._curr_obj = None
        self._wapped_class = wapped_class
        self._wapped_args = wapped_args
        self._style_template_class = style_template_class
        self._style_template = None
    def has_next(self):
        return self._length != 0 and self._index < self._length
    def items(self):
        return self._iterable
    def __iter__(self):
        while self._index < self._length:
            self._curr_obj = self._iterable[self._index]
            self._index = self._index + 1
            yield self._wapped_class(self._curr_obj, **self._wapped_args) \
                    if self._wapped_args else self._wapped_class(self._curr_obj)
    
    
    def _check_template_style(self):
        if not self._style_template:
            if self._style_template_class:
                self._style_template = self._style_template_class(self) 
            else:self._style_template= find_template_style(self._wapped_class, self)
    def list_items(self, **styles):
        self._check_template_style()
        rv = self._style_template.render(**styles)
        return rv;
    def __getattr__(self, key):
        self._check_template_style()
        if  key not in  self.__dict__:
            if self._style_template:
                return getattr(self._style_template, key)
        return self.__dict__.get(key)
    def next_link(self):
        pass
    
class StyleTemplate(object):
    _styles = {
            'container': None,
            'container_class' :None,
            'parent': None,
            'deli':None,
            'parent_class':None,
            'class': []
            }
    def __init__(self, items):
        self._items = items
        self.set_style(**self._styles)
    def render(self, **styles):
        if len(styles) > 0:
            self.set_style(**styles)
        out = root = None
        if self._parent:
            root = tag(self._parent, **{'class':self._parent_cls})
        childrens = []
        for item in self._items:
            rv = None
            if self._container:
                rv = self._make_container(item)
                rv.add_children(self._make_link(item))
            else:
                rv = self._make_link(item)
            childrens.append(rv)
        deli = self._deli or ''
        out = deli.join([item.render() for item in childrens])
        if root:
            root.body = out
            return root.render()
        else:
            return out
                
    def get_style(self, key):
        return self._styles.get(key, '')
    def set_style(self, **args):
        if len(args) > 0:
            self._styles.update(args)
        self._parent = self.get_style('parent')
        self._parent_cls = self.get_style('parent_class')
        self._class = self.get_style('class')
        self._container = self.get_style('container')
        self._container_cls = self.get_style('container_class')
        self._deli = self.get_style('deli')
        return '' # for  jinja2 hack
    def _get_url(self, item):
        pass
    def _get_title(self, item):
        pass
    def _render(self, item, tagName,  class_,body=None ,**attrs):
        attrs.update({
                     'class':class_
                     })
        rv = tag(tagName,
                    **attrs
                 )
        if body :
            rv.body = body
        return rv;
    def _make_container(self, item, **args):
        return self._render(item, self._container, self._container_cls, **args)
    def _make_link(self, item, **args):
        args.update({
                     'href':self._get_url(item)
                    }
                    )
        return self._render(item, 'a',
                            body=self._get_title(item),
                            class_=self._class,
                            **args
                            )
'''   
class BaseStyleTemplate(StyleTemplate):
    def __init__(self, url_for, title_attr, **styles):
        self._url_for = url_for
        self._title_attr = title_attr
        self.set_style(**styles)
    def _get_url(self, item):
        return self._url_for(item)
    def _get_title(self, item):
        return getattr(item, self._title_attr)
'''
class WappedObjectStyleTemplate(StyleTemplate):
    def __init__(self, items):
        StyleTemplate.__init__(self, items)
        #
    def _get_url(self, item): 
        linkfunc = getattr(item, 'the_permalink')
        if not linkfunc:
            raise TypeError('object must be has the_permalink attr')
        return linkfunc()
    def _get_title(self, item): 
        namefunc = getattr(item, 'the_name')
        if not namefunc:
            raise TypeError('object must be has the_permalink attr')
        return namefunc()

class CommentStyleTemplate(StyleTemplate):
    _styles = {
            'parent': 'ol',
            'parent_class':['comment-list'],
            'container': 'li',
            'author_widget':'system.author.info',
            'container_class':['comment-body', 'comment-odd'],
            'comment_parent_class':['comment-parent'],
            'comment_children_class':['comment-child', 'comment-level-odd', 'comment-by-author'],
            'comment_children_parent':'div',
            'comment_children_parent_class':['comment-children'],
            'show_avatar':True,
            'author_tag':'div',
            'author_class':['comment-author'],
            'comment_meta_tag':'div',
            'comment_meta_class':['comment-meta'],
            'allow_replay_level':5,
            'replay_tag': 'div',
            'replay_class' :['comment-reply'],
            'fetch_children':True,
            'fetch_children_level':5,
            'class': None,
            'replay_title':'replay',
            'cancel_replay_title':'Click here to cancel reply.'
            }
    def __init__(self, items):
        StyleTemplate.__init__(self, items)
    def set_style(self, **args):
        StyleTemplate.set_style(self, **args)
        try:
            self._allow_replay_level = int(self.get_style('allow_replay_level'))
        except:
            self._allow_replay_level = 5
        try:
            self._fetch_children_level = self.get_style('fectch_children_level')
        except:
            self._fetch_children_level = 5
        return ''
       	
    @classmethod
    def register_js(cls, respond_id):
        ctx._js('comment_helper',
                '''
                /* the script copyright by  typecho */
                var CommentHelper = {
                    dom : function (id) {
                        return document.getElementById(id);
                    },
                    
                    create : function (tag, attr) {
                        var el = document.createElement(tag);
                        
                        for (var key in attr) {
                            el.setAttribute(key, attr[key]);
                        }
                        
                        return el;
                    },
                
                    reply : function (cid, coid) {
                        var comment = this.dom(cid), parent = comment.parentNode,
                            response = this.dom('%s'), input = this.dom('comment-parent'),
                            form = 'form' == response.tagName ? response : response.getElementsByTagName('form')[0],
                            textarea = response.getElementsByTagName('textarea')[0];
                
                        if (null == input) {
                            input = this.create('input', {
                                'type' : 'hidden',
                                'name' : 'parent',
                                'id'   : 'comment-parent'
                            });
                
                            form.appendChild(input);
                        }
                        
                        input.setAttribute('value', coid);
                
                        if (null == this.dom('comment-form-place-holder')) {
                            var holder = this.create('div', {
                                'id' : 'comment-form-place-holder'
                            });
                            
                            response.parentNode.insertBefore(holder, response);
                        }
                
                        comment.appendChild(response);
                        this.dom('cancel-comment-reply-link').style.display = '';
                        
                        if (null != textarea && 'text' == textarea.name) {
                            textarea.focus();
                        }
                        
                        return false;
                    },
                
                    cancelReply : function () {
                        var response = this.dom('%s'),
                        holder = this.dom('comment-form-place-holder'), input = this.dom('comment-parent');
                
                        if (null != input) {
                            input.parentNode.removeChild(input);
                        }
                
                        if (null == holder) {
                            return true;
                        }
                
                        this.dom('cancel-comment-reply-link').style.display = 'none';
                        holder.parentNode.insertBefore(response, holder);
                        return false;
                    }
                }
                '''
                % (respond_id, respond_id)
                )

    def render(self, **args):
    	StyleTemplate.set_style(self, **args)
        rv = self._render_by(self._items, 1)
        self.register_js(self.respond_id())
        return rv.render()
    def _render_by(self, items, level=1):
        parent_tag = self._parent or 'ol'
        parent = tag(parent_tag, **{
                                  'class':self._parent_cls[0:]
                                  })
        for  item in  items :
            rv = self._render(item, level)
            parent.add_children(rv)
        return parent
    def _render(self, item, level=1):
        container = None
        container_tag = self._container or 'li'
        container = tag(container_tag,
                              **{'class':self._container_cls[0:],
                                 'id':'comment-%s' % (item.the_id())
                                })
        #是否显示头像
        author = None
        if self.get_style('show_author'):
            author_tag = self.get_style('author_tag')  or  'div'
            author_cls = self.get_style('author_class')
            author = tag(author_tag, **{
                                       'class': author_cls[0:]
                                       })
            author_widget = self.get_style('author_widget')
            author_html = ctx.plugin_manager.\
                find_widget(author_widget, mail=item.the_email(), **self._styles).parse()
            if author_html:
                author.body = author_html
        if author:
            container.add_children(author)
        #评论meta
        comment_meta = ''
        comment_meta_tag = self.get_style('comment_meta_tag') or 'div'
        comment_meta_cls = self.get_style('comment_meta_class')
        comment_meta = tag(comment_meta_tag, **{
                                               'class':comment_meta_cls[0:]
                                               })
        comment_meta_body = tag('a')
        comment_meta_body.rel = 'nofollow'
        comment_meta_body.href = '#comment-%d' % item.the_id()
        comment_meta_body.body = item.the_time()
        if level > 1:
            container.update('class', self.get_style('comment_children_class')[0:])
        comment_meta.add_children(comment_meta_body);
        
       # container.add_children(author)
        container.add_children(comment_meta)
        content = Span(item.the_content(), **{
                                             'class':'comment-content'
                                             })
        #content  = span(item.the_content())
        container.add_children(content)
        
        if self.get_style('fetch_children') :
            if level < self._fetch_children_level and item.have_children():
                container.update('class', self.get_style('comment_parent_class')[0:])
                children_layer_tag = self.get_style('comment_children_parent') or 'div'
                children_layer = tag(children_layer_tag, **{
                                         'class':self.get_style('comment_children_parent_class')
                                   })
                container.add_children(children_layer)
                children_layer.add_children(self._render_by(item.childrens(), level + 1))
        if level <= self._allow_replay_level :
            replay = tag(self.get_style('replay_tag'), **{
                                'class':self.get_style('replay_class')
                                                           })
            replay_body = tag('a', **{
                                        'class':'replay',
                                        'href':'#',
                                        'rel':'nofollow',
                                        'onclick':'''return CommentHelper.reply('%s',%d)''' \
                                                    % ('comment-%s' % item.the_id(),
                                                      item.the_id()
                                                      )
                                        })
            replay_body.body = self.get_style('replay_title')
            replay.add_children(replay_body)
            container.add_children(replay)        
        return  container
            
    def respond_id(self):
        return  'comment-respond-%s' % str(id(self))
        
    def cancel_reply(self):
        cancel_comment_replay = Div(**{
                                       'id':'cancel_comment_reply'
                                       }
                                    )
        cancel_comment_replay.add_children(A(body=self.get_style('cancel_replay_title'),
                                              **{
                                                'id':'cancel-comment-reply-link',
                                                'href':'#',
                                                'rel':'nofollow',
                                                'style':'display:none',
                                                'onclick':'return CommentHelper.cancelReply();'
                                                }
                                              )
                                           )
        return cancel_comment_replay.render()
class Page(StyleTemplate):
    _styles = {
             'parent': 'ol',
             'parent_class':'page-navigator',
             'container':'li',
             'container_class':['page-nav'],
             'class':[],
             'prev_title':'prev',
             'next_title':'next',
             'show_prev':True,
             'show_next':True,
             'curr_class':['current'],
             'next_class':['next'],
             'prev_class':['prev']
             }
    def  __init__(self, totalItems, currentPage=1, limit=1, url_for=None):
        StyleTemplate.__init__(self, self)
        if limit is None or  limit <= 0:
            limit = 5
        self._limit = int(limit) if  limit and limit >= 0 else 10
        self._totalItems = int(totalItems) if not totalItems else 0
        self._currentPage = int(currentPage) if  currentPage and currentPage >= 0 else 1
        self._pages = totalItems / self._limit if totalItems % self._limit == 0 else totalItems / self._limit + 1
        self._totalItems = totalItems
        self._url_for = url_for
        if self._pages == 0:
            self._pages = 1
        if self._currentPage > self._pages:
            self._currentPage = self._pages
    def set_style(self, **styles):
        StyleTemplate.set_style(self, **styles)
        self._prev_title = self.get_style('prev_title')
        self._next_title = self.get_style('next_title')
        self._show_prev = self.get_style('show_prev')
        self._show_next = self.get_style('show_next')
        self._curr_class = self.get_style('curr_class')
        self._next_class = self.get_style('next_class')
        self._prev_class = self.get_style('prev_class')
    def totle_items(self):
        return self._totalItems
    
    def totle_pages(self):
        return self._pages
    def limit(self):
        return self._limit
    def has_next(self):
        if self._currentPage >= self._pages:
            return False
        return True
    def prev_link(self, *arg, **kwords):
        link_obj = self._prev_link(*arg, **kwords)
        return link_obj.render() if link_obj else ''
    def next_link(self, *arg, **kwords):
        link_obj = self._next_link(*arg, **kwords)
        return link_obj.render() if link_obj else ''
    def _build_link(self, class_, pageNum, title):
        href = str(pageNum) if not self._url_for else self._url_for(pageNum)
        return A(body=title,
                        **{
                            'class':class_,
                            'href':href
                           }
                )
    def _prev_link(self, *arg, **kwords):
        if not self.has_prev():return None
        else:
            title = None
            if len(arg) < 0:
                title = kwords.pop('title', str(self.prev_page()))
            else:
                title = arg[0]
            class_ = kwords.pop('class', None)
            if class_:
                if not isinstance(class_, (list, tuple)):
                    class_ = [class_]
            else:
                class_=[]
            class_.extend(self._next_class)
            pageNum = str(self.prev_page())
            rv = None
            if self._container:
                rv = self._make_container(pageNum, class_=class_)
                rv.add_children(self._make_link(pageNum, body=title))
            else:
                rv = self._make_link(pageNum, body=title, class_=class_)
            return rv
        
    def _next_link(self, *arg, **kwords):
        if not self.has_next():return None
        else:
            title = None
            if len(arg) < 0:
                title = kwords.pop('title', str(self.next_page()))
            else:
                title = arg[0]
            class_ = kwords.pop('class', None)
            if class_:
                if not isinstance(class_, (list, tuple)):
                    class_ = [class_]
            else:
                class_=[]
            class_.extend(self._next_class)
            pageNum = str(self.next_page())
            rv = None
            if self._container:
                rv = self._make_container(pageNum, class_=class_)
                rv.add_children(self._make_link(pageNum, body=title))
            else:
                rv = self._make_link(pageNum, body=title, class_=class_)
            return rv
    def has_prev(self):
        if self._currentPage <= 1:
            return False
        return True
    def next_page(self):
        if self._currentPage < self._pages:
            return self._currentPage + 1
        else:
            return None
    def prev_page(self):
        if self._currentPage == 1:
            return 1
        else:
            return self._currentPage - 1
    def curr_page(self):
        return self._currentPage
    def count(self):
        return self._totalItems
    def curr_offset(self):
        if self._currentPage >= 1:
            return (self._currentPage - 1) * self._limit
        else:
            return 0
    def _make_container(self, item, class_=None, **args):
        cls = self._container_cls[0:]
        if not class_:
            co = int(item)
            if co == self.curr_page():
                cls.extend(self._curr_class[0:])
        else:
            cls.extend(class_)
        return self._render(item, self._container, cls, **args)
    def _make_link(self, item, body=None, class_=None, **args):
        body = body or item
        class_ = class_ or self._class
        href = self._url_for(item) if self._url_for else item
        args.update({
                     'title':'navigator-page-%s' % item,
                     'href':href
                     })
        return self._render(item,
                            'a',
                            class_,
                            body=body,
                           **args)
    def paging(self,**styles):
        return self.render(**styles)
    def render(self, **styles):
        if self.totle_pages() == 0 or self.totle_pages() == 1:
            return ''
        if len(styles) > 0:
            self.set_style(**styles)
        out = root = None
        if self._parent:
            root = tag(self._parent, **{'class':self._parent_cls})
        childrens = []
        for item in self._items:
            rv = None
            if self._container:
                rv = self._make_container(item)
                rv.add_children(self._make_link(item))
            else:
                rv = self._make_link(item)
            childrens.append(rv)
        if self._show_prev and self.has_prev():
            childrens.insert(0, self._prev_link(self._prev_title))
        if self._show_next and self.has_next():
            childrens.append(self._next_link(self._next_title))
        deli = self._deli or ''
        out = deli.join([item.render() for item in childrens])
        if root:
            root.body = out
            return root.render()
        else:
            return out
        
    def _get_url(self, item):
        if self._url_for:
            return self._url_for(item)
        return item
    def _get_title(self, item):
        return item
    '''
    def _render(self, item,tagName,body,class_,**attrs):
    
        attrs.update({
                     'class':class_
                     })
        rv = tag(tagName,
                    **attrs
                 )
        if body :
            rv.body = body
        return rv;
    '''
    def __iter__(self):
        index = 0
        while index < self.totle_pages():
            index += 1 
            yield str(index)
    '''
    def nav(self,
            cls='page-navigator',
            prev_title="prev",
            next_title="next",
            rate=10,
            show_prev=True,
            show_next=True,
            prev_cls="prev",
            next_cls='next',
            curr_cls='current'
            ):
        def nav_link(linkclass_, pageNum, title, class_='nav'):
            return '<li class=%s>%s</li>' % (class_, self._build_link(linkclass_, pageNum, title))
        navs = []
        if show_prev and self.has_prev():
            navs.append(nav_link(prev_cls, self.prev_page(), prev_title))
        try:
            rate = int(rate)
        except:
            rate = 10
        _range = self.totle_pages() if rate > self.totle_pages() else rate
        _cls = 'nav-like'
        for i  in range(0, _range):
            _loop = i + 1
            if  _loop == self.curr_page():
                navs.append(nav_link(_cls, _loop, str(_loop), curr_cls))
            else:
                navs.append(nav_link(_cls, _loop, str(_loop)))
        if self.totle_pages() > rate:
            navs.append('...')
        if self.has_next() and show_next:
            navs.append(nav_link(next_cls, self.next_page(), next_title))
        if isinstance(cls, (tuple, list)):
            cls = ' '.join(cls)
        return '<ol class=%s>%s</ol>' % (cls, '\r\n'.join(navs))
    '''
def  find_template_style(cls_, items):
    kind = ''
    if cls_ == WappedMeta:
        kind = 'meta'
    return DEFAULT_TEMPLATE_STYLE[kind](items)
DEFAULT_TEMPLATE_STYLE = {
                    'meta':WappedObjectStyleTemplate
                    }

if __name__ == '__main__':
    from schema import session
    from models import Comment
   
    replay = tag('div', **{
                                'class':'div'
                            })
    replay_body = A(href='#')
    replay.add_children(replay_body)
    print replay.render()
