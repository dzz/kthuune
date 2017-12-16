from Beagle import API as BGL

class TitleBar:
    shader = BGL.assets.get('KT-editor/shader/titlebar')
    primitive = BGL.primitive.unit_uv_square

    def render(app):
        TitleBar.primitive.render_shaded( TitleBar.shader, {} )

