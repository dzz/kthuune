from .Brushes import Brushes
from .GeneratedArea import GeneratedArea
from .PolyFillList import PolyFillList
from .LevelPreview import LevelPreview

class World:
    Brushes = Brushes
    GeneratedArea = GeneratedArea

    def find_limits():
        #find a square area that fits the entire world

        limit = 0
        for brush in World.Brushes.brushes:
            limit = max(abs(brush.x1),limit)
            limit = max(abs(brush.y1),limit)
            limit = max(abs(brush.x2),limit)
            limit = max(abs(brush.y2),limit)
             
        World.GeneratedArea.width = limit*2 #1 in brush space == 2 in gamespace, w/h <>
        World.GeneratedArea.height = limit*2

    def reduce():

        World.GeneratedArea.reset()

        World.find_limits()
        polyfill_map = PolyFillList.getPolyFillMap()

        for brush in World.Brushes.brushes:
            if brush.polyfill_key in polyfill_map:
                polyfill = polyfill_map[brush.polyfill_key]
                polyfill.reduce( World.GeneratedArea, brush )

        World.GeneratedArea.serialize()

        LevelPreview.reset( World.GeneratedArea.output_data )

        
