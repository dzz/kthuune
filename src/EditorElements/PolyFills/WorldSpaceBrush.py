class WorldSpaceBrush:
    def from_brush(brush):
        wsb = WorldSpaceBrush()
        wsb.x1 = brush.x1*2.0
        wsb.y1 = brush.y1*2.0
        wsb.x2 = brush.x2*2.0
        wsb.y2 = brush.y2*2.0
        wsb.cx = (wsb.x2+wsb.x1)/2.0
        wsb.cy = (wsb.y2+wsb.y1)/2.0
        return wsb

