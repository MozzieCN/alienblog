from contrlib import plugin
from contrlib.plugin import DONE

class CategoryWidget(plugin.Widget):
    def __init__(self):
        plugin.Widget.__init__(self,'system.category.widget')
    def do(self,**args):
        app= self.framework.curr_app
        categoris = self.framework.do_action('system.show.categories',
                                        appid=app.id
                                        )
        return categoris
