from contrlib import plugin

class CategoryWidget(plugin.Widget):
    def __init__(self):
        plugin.Widget.__init__(self,'system.category.widget')
    def parse(self,**args):
        pool  = self.do()
        if pool:
            return pool.list_items(**args)
    def do(self,**args):
        from alien import current_app,ctx
        from view_models import WappedPool,WappedMeta
        metas = ctx.plugin_manager.do_action('system.show.metas',
                                     appId=current_app.id,
                                     type='category'
                                     )
        if metas:
            return WappedPool(metas,WappedMeta,
                                    **{
                                       'url_for':
                                       ctx.category_url_for
                                       })
