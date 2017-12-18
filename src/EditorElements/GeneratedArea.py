from random import choice

class GeneratedArea:
    width = 0
    height = 0
    output_data = ""
    tiles = {}
    shadow_tiles = [ 59,60 ]

    def reset():
        GeneratedArea.output_data = ""
        GeneratedArea.extra = ""
        GeneratedArea.tiles = {}

    def set_tile(x,y,value, brush = None):

        if brush:
            if x < brush.x1: return
            if x > brush.x2: return
            if y < brush.y1: return
            if y > brush.y2: return

        GeneratedArea.tiles[(int(x),int(y))] = value
        pass

    def add_line(line):
        GeneratedArea.output_data = "{0}{1}\n".format(GeneratedArea.output_data,line)
        
    def serialize_model():
        GeneratedArea.add_line("MODEL")
        GeneratedArea.add_line("{0}".format(GeneratedArea.width))
        GeneratedArea.add_line("{0}".format(GeneratedArea.height))

    def serialize_tiles():
        limit = int(GeneratedArea.width/2)
        for x in range( -1 * limit, limit):
            for y in range( -1 * limit, limit):
                if (x,y) in GeneratedArea.tiles:
                    GeneratedArea.add_line("TILE")
                    GeneratedArea.add_line("{0}".format(x))
                    GeneratedArea.add_line("{0}".format(y))
                    GeneratedArea.add_line("{0}".format(GeneratedArea.tiles[(x,y)]))
                else:
                    if (x,y-1) in GeneratedArea.tiles:
                        GeneratedArea.add_line("TILE")
                        GeneratedArea.add_line("{0}".format(x))
                        GeneratedArea.add_line("{0}".format(y))
                        GeneratedArea.add_line("{0}".format(choice( GeneratedArea.shadow_tiles)))

    def serialize_player():
        GeneratedArea.add_line("OBJECT")
        GeneratedArea.add_line("player_start")
        GeneratedArea.add_line("0")
        GeneratedArea.add_line("0")
        GeneratedArea.add_line("{}")

    def serialize():
        GeneratedArea.serialize_model()
        GeneratedArea.serialize_tiles()
        GeneratedArea.serialize_player()
        print(GeneratedArea.output_data)


