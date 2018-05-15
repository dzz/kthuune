from Beagle import API as BGL
from .PolyFillList import PolyFillList
from math import floor
from .Brushes import Brushes
from .Brush import Brush
from .PolyFills.layer_map import layer_map

class PolyFillMenu:
    mx = 0
    my = 0
    hover_item = None

    def render(app):
        with BGL.blendmode.alpha_over:
            BGL.lotext.render_text_pixels("Brush Polyfill", 5, 18, [1.0,1.0,1.0])
            BGL.lotext.render_text_pixels("--------------", 5, 27, [1.0,1.0,1.0])

        base_list = PolyFillList.getPolyFills(app.layer)
        base_list.sort()
        base_list.sort( key = lambda key: PolyFillList.getPolyFill(key).layer )

        for idx,polyfill in enumerate(base_list):

            layer = PolyFillList.getPolyFill(polyfill).layer
            lf = (float(layer%4) / 5.0 ) + (1.0/5.0)
            mf = (float((8-layer)%6) / 4.0) + (1.0/4.0)
            hf = (float((5-layer)%3) / 4.0) + (1.0/4.0)
            color = [ lf,hf,mf ]
            menu = PolyFillMenu
            base_px = 38
            item = None
            row_px = 5
            hover_item = None
            if(menu.my>base_px):
                item = floor((menu.my-base_px)/9)
                if idx == item:
                    color = [ 1.0,1.0,1.0 ]
                    menu.hover_item = polyfill
                    base_px -= 1
                    row_px += 1
                    polyfill = polyfill.upper()
            BGL.lotext.render_text_pixels("{0} {1}".format(layer,polyfill), row_px, base_px+(9*idx)-1, [0.0,0.0,0.0] )
            BGL.lotext.render_text_pixels("{0} {1}".format(layer,polyfill), row_px, base_px+(9*idx), color )

    def dispatch_mousemotion(app, x, y):
        menu = PolyFillMenu
        menu.mx = floor(x / 2)
        menu.my = floor(y / 2)

    def dispatch_mousedown(app, button, x, y):
        Brush.set_template_polyfill( PolyFillMenu.hover_item )
        Brushes.set_polyfill( PolyFillMenu.hover_item )
        
        
