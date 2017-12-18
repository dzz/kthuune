import json
class Factory:
    def make_light( area, x, y, light_class ):
        area.add_line("OBJECT")
        area.add_line("light") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"class":light_class})) #meta line
        area.add_line("True") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_edges( area, edges, physics = True, lights = True, decoration = False ):
        for edge in edges:
            area.add_line("LINE")
            area.add_line("{0}".format(edge[0]*2.0))
            area.add_line("{0}".format(edge[1]*2.0))
            area.add_line("{0}".format(edge[2]*2.0))
            area.add_line("{0}".format(edge[3]*2.0))
            area.add_line("{0}".format(lights))
            area.add_line("{0}".format(physics))
            area.add_line("{0}".format(decoration))
            
    def make_totem( area, x, y):
        area.add_line("OBJECT")
        area.add_line("totem") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height
