from Beagle import API as BGL

class Editor:
    ui_fb = BGL.framebuffer.from_dims(852, 480)
    def __init__(self):
        pass

    def configure(self, config):
        pass

    def init(self):
        self.__mouse_position__ = self.__shell__['__mpos']
        pass

    def tick(self):
        pass

    def render(self):
        with BGL.context.render_target(Editor.ui_fb):
            BGL.context.clear(0.0,0.0,0.0,0.0)
            with BGL.blendmode.alpha_over:
                BGL.lotext.render_text_pixels("-=~ EDITOR =-~ {0} {1}".format(self.__mouse_position__[0], self.__mouse_position__[1]), 0,0, [0.0,1.0,0.0])

        BGL.context.clear(0.0,0.0,0.0,0.0)
        with BGL.blendmode.alpha_over:
            Editor.ui_fb.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))
        pass

    def finalize(self):
        pass
