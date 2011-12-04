from contrlib import plugin
from contrlib.plugin import DONE

class HeadWidget(plugin.Widget):
    def __init__(self):
        plugin.Widget.__init__(self,'head')
    def do(self,**args):
        return self.framework.render('head',**{})
