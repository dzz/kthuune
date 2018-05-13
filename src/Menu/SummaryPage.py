from Beagle import API as BGL
from .Menu import Menu

class SummaryPage():
    texture_header = BGL.assets.get("KT-player/texture/level_summary")
    def __init__(self,floor):
        self.floor = floor
        self.t = 0
        self._t = 0 

    def tick(self):
        self.t = self.t + 1
        self._t += 0.003;

        if(self.t<270):
            return self

    def render(self):
        with BGL.blendmode.alpha_over:
            Menu.primitive.render_shaded( Menu.shader, {
                "texBuffer" : SummaryPage.texture_header,
                "tick" : self.t
            })

