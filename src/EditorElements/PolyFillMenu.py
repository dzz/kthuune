from Beagle import API as BGL
from .PolyFillList import PolyFillList
from math import floor
from .Brushes import Brushes
from .Brush import Brush

class PolyFillMenu:
    mx = 0
    my = 0
    hover_item = None

    def render(app):
        with BGL.blendmode.alpha_over:
            BGL.lotext.render_text_pixels("Brush Polyfill", 5, 18, [1.0,1.0,1.0])
            BGL.lotext.render_text_pixels("--------------", 5, 27, [1.0,1.0,1.0])

        for idx,polyfill in enumerate(PolyFillList.getPolyFills()):
            color = [ 0.5,0.5,0.5 ]
            menu = PolyFillMenu
            base_px = 38
            item = None

            hover_item = None
            if(menu.my>base_px):
                item = floor((menu.my-base_px)/9)
                if idx == item:
                    color = [ 1.0,1.0,1.0 ]
                    menu.hover_item = polyfill
            BGL.lotext.render_text_pixels(polyfill, 5, base_px+(9*idx), color )

    def dispatch_mousemotion(app, x, y):
        menu = PolyFillMenu
        menu.mx = floor(x / 2)
        menu.my = floor(y / 2)

    def dispatch_mousedown(app, button, x, y):
        Brush.set_template_polyfill( PolyFillMenu.hover_item )
        Brushes.set_polyfill( PolyFillMenu.hover_item )
        
        
