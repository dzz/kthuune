class Brush:
    next_id = 1
    template_polyfill = "None"

    def get_next_id():  
        r = Brush.next_id
        Brush.next_id+=1
        return r
    
    def __init__(self):
        self.id = Brush.get_next_id()
        self.x1 = None
        self.y1 = None
        self.x2 = None 
        self.y2 = None 
        self.layer = 0
        self.polyfill_key = Brush.template_polyfill

    def set_template_polyfill(key):
        Brush.template_polyfill = key

    def from_tool(tool):
        b = Brush()
        b.x1 = tool.x1
        b.y1 = tool.y1
        b.x2 = tool.x2
        b.y2 = tool.y2
        return b



