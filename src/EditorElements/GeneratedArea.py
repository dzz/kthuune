class GeneratedArea:
    width = 0
    height = 0
    output_data = ""
    tiles = {}

    def reset():
        GeneratedArea.output_data = ""
        GeneratedArea.tiles = {}

    def set_tile(x,y,value):
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
                GeneratedArea.add_line("TILE")
                GeneratedArea.add_line("{0}".format(x))
                GeneratedArea.add_line("{0}".format(y))
                if (x,y) in GeneratedArea.tiles:
                    GeneratedArea.add_line("{0}".format(GeneratedArea.tiles[(x,y)]))
                else:
                    GeneratedArea.add_line("{0}".format(0))

    def serialize_player():
        GeneratedArea.add_line("OBJECT")
        GeneratedArea.add_line("player_start")
        GeneratedArea.add_line("0")
        GeneratedArea.add_line("0")
        GeneratedArea.add_line("{}")

    def serialize():
        GeneratedArea.output_data = ""
        GeneratedArea.serialize_model()
        GeneratedArea.serialize_tiles()
        GeneratedArea.serialize_player()
        print(GeneratedArea.output_data)


