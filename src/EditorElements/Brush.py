class Brush:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None 
        self.y2 = None 
        self.layer = 0
        self.generator_key = None

    def from_tool(tool):
        b = Brush()
        b.x1 = tool.x1
        b.y1 = tool.y1
        b.x2 = tool.x2
        b.y2 = tool.y2
        return b
