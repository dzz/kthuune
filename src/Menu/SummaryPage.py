from Beagle import API as BGL
from .Menu import Menu
from math import floor

class SummaryPage():
    texture_header = BGL.assets.get("KT-player/texture/level_summary")
    texbuffer = BGL.framebuffer.from_dims( 240, 135 )
    Time = 420 #how many frames to show summary
    TIME_MULTIPLIER = 50  
    KILL_MULTIPLIER = 125

    def __init__(self,floor):
        self.floor = floor
        self.t = 0
        self._t = 0 
        self.alpha = 0.0
        self.remaining_time = floor.player.life_timer / 60.0
        self.total_kills = floor.player.total_kills
        self.slash_remainder = floor.slash_limit - floor.player.total_slashes

        self.time_bonus = 0
        self.kill_bonus = 0
        self.slash_bonus = 0
        self.total_points = 0

    def compute_total(self):
        return self.time_bonus + self.kill_bonus * (self.slash_bonus+1)

    def tick(self):

        if(self.t > 10 ):
            if(self.remaining_time>0):
                self.time_bonus += SummaryPage.TIME_MULTIPLIER
                self.remaining_time -= 1

        if(self.t > 30 ):
            if(self.total_kills>0):
                self.kill_bonus += SummaryPage.KILL_MULTIPLIER
                self.total_kills -= 1

        if( self.t> 60 ):
            total = self.compute_total()
            if(self.total_points < total):
                self.total_points += 25
            if(self.total_points < (total-500)):
                self.total_points += 500
            if(self.total_points < (total-100)):
                self.total_points += 100

        if( self.t> 80 ):
            if(floor(self.slash_bonus) < self.slash_remainder):
                self.slash_bonus += 0.1

        self.t = self.t + 1
        self._t += 0.003;
        if(self.alpha<1.0):
            self.alpha += 1.0/120.0

        if(self.t<SummaryPage.Time):
            return self

    def render(self):
        with BGL.context.render_target( SummaryPage.texbuffer ):
            with BGL.blendmode.alpha_over:
                BGL.context.clear(  0.0,0.0,0.0,0.0 )

                if(self.time_bonus>0):
                    bonus = "TIME BONUS: {0}".format(self.time_bonus)
                    BGL.lotext.render_text_pixels(bonus, 35, 30, [ 0.0,0.0,0.0] )
                    BGL.lotext.render_text_pixels(bonus, 36, 31, [ 1.0,1.0,1.0] )

                if(self.kill_bonus>0):
                    bonus = "KILL BONUS: {0}".format(self.kill_bonus)
                    BGL.lotext.render_text_pixels(bonus, 35, 40, [ 0.0,0.0,0.0] )
                    BGL.lotext.render_text_pixels(bonus, 36, 41, [ 1.0,1.0,1.0] )

                if(self.slash_bonus>0):
                    bonus = "SLASH MUL:{0:.2f}X!".format(self.slash_bonus)
                    BGL.lotext.render_text_pixels(bonus, 35, 50, [ 0.0,0.0,0.0] )
                    BGL.lotext.render_text_pixels(bonus, 36, 51, [ 1.0,1.0,1.0] )

                if(self.total_points>0):
                    bonus = "total purity:{0}".format(self.total_points)
                    BGL.lotext.render_text_pixels(bonus, 35, 70, [ 0.0,0.0,0.0] )
                    BGL.lotext.render_text_pixels(bonus, 36, 71, [ 1.0,1.0,1.0] )

        with BGL.blendmode.alpha_over:
            Menu.primitive.render_shaded( Menu.shader, {
                "texBuffer" : SummaryPage.texture_header,
                "tick" : self._t,
                "alpha" : self.alpha
            })
            SummaryPage.texbuffer.render_processed(BGL.assets.get("beagle-2d/shader/passthru"))

