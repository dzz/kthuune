from Beagle import API as BGL

class Fog:
    primitive = BGL.primitive.unit_uv_square
    shader = BGL.assets.get("KT-compositor/shader/fog")
    def render(self, floor, vision_tex, fog_level):
        with BGL.blendmode.alpha_over:
            Fog.primitive.render_shaded( Fog.shader, {
                "light_buffer" : floor.light_buffer,
                "camera_position" : self.camera.p,
                "parallax" : [ 2.0 ],
                "tick" : floor._tick,
                "vision_tex" : vision_tex,
                "fog_level" : fog_level
            } )
            Fog.primitive.render_shaded( Fog.shader, {
                "light_buffer" : floor.light_buffer,
                "camera_position" : self.camera.p,
                "parallax" : [ 3.0 ],
                "tick" : floor._tick,
                "vision_tex" : vision_tex,
                "fog_level" : fog_level
            } )
            Fog.primitive.render_shaded( Fog.shader, {
                "light_buffer" : floor.light_buffer,
                "camera_position" : self.camera.p,
                "parallax" : [ 4.0 ],
                "tick" : floor._tick,
                "vision_tex" : vision_tex,
                "fog_level" : fog_level
            } )
        return True
