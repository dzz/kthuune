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
            
    def make_totem( area, x, y, group, shield = False):
        area.add_line("OBJECT")
        area.add_line("totem") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"group":group, "shield":shield}))
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_playerstart( area, x, y):
        area.add_line("OBJECT")
        area.add_line("player_start") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_chargeplate( area, x, y, group):
        area.add_line("OBJECT")
        area.add_line("chargeplate") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"group":group}))
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_skeline( area, x, y, group):
        area.add_line("OBJECT")
        area.add_line("skeline") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"group":group}))
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_acolyte( area, x, y, group):
        area.add_line("OBJECT")
        area.add_line("acolyte") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"group":group}))
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_cleric( area, x, y, group):
        area.add_line("OBJECT")
        area.add_line("cleric") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line(json.dumps({"group":group}))
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_lantern( area, x, y):
        area.add_line("OBJECT")
        area.add_line("lantern") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_stainglass( area, x, y):
        area.add_line("OBJECT")
        area.add_line("stainglass") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_firepot_up( area, x, y):
        area.add_line("OBJECT")
        area.add_line("firepot_up") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_firepot_down( area, x, y):
        area.add_line("OBJECT")
        area.add_line("firepot_down") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_firepot_right( area, x, y):
        area.add_line("OBJECT")
        area.add_line("firepot_right") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_firepot_left( area, x, y):
        area.add_line("OBJECT")
        area.add_line("firepot_left") #object type
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y)) 
        area.add_line("{}")
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_hostages( area, brush):
        for x in range( brush.x1, brush.x2 ):
            for y in range( brush.y1, brush.y2 ):

                if(x%2==0):
                    continue
                if(y%2==0):
                    continue
                if((x+y)%3==1):
                    continue

                area.add_line("OBJECT")
                area.add_line("hostage") #object type
                area.add_line("{0}".format(x*2))
                area.add_line("{0}".format(y*2)) 
                area.add_line("{}")
                area.add_line("False") #is region
                area.add_line("0") #width
                area.add_line("0") #height

    def make_door( area, x1,y1, x2,y2, uid ):
        area.add_line("OBJECT")
        area.add_line("door_pin") #object type
        area.add_line("{0}".format(x1))
        area.add_line("{0}".format(y1)) 
        area.add_line(uid)
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height
        area.add_line("OBJECT")
        area.add_line("door_end") #object type
        area.add_line("{0}".format(x2))
        area.add_line("{0}".format(y2)) 
        area.add_line(uid)
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height
        area.add_line("OBJECT")
        area.add_line("door_sensor") #object type
        area.add_line("{0}".format((x2+x1)/2))
        area.add_line("{0}".format((y2+y1)/2)) 
        area.add_line(uid)
        area.add_line("False") #is region
        area.add_line("0") #width
        area.add_line("0") #height

    def make_blindarcade( area, x1,y1,x2,y2):
        area.add_line("OBJECT")
        area.add_line("blindarcade") #object type
        area.add_line("{0}".format(x1))
        area.add_line("{0}".format(y1)) 
        area.add_line(json.dumps({})) #meta line
        area.add_line("True") #is region
        area.add_line("{0}".format(x2)) #w/h ... but we're abusing it for a position
        area.add_line("{0}".format(y2)) 

    def make_treetrunk( area, x1,y1,x2,y2):
        area.add_line("OBJECT")
        area.add_line("treetrunk") #object type
        area.add_line("{0}".format(x1))
        area.add_line("{0}".format(y1)) 
        area.add_line(json.dumps({})) #meta line
        area.add_line("True") #is region
        area.add_line("{0}".format(x2)) #w/h ... but we're abusing it for a position
        area.add_line("{0}".format(y2)) 

    def make_decorator( area, x1,y1,x2,y2):
        area.add_line("OBJECT")
        area.add_line("decorator") #object type
        area.add_line("{0}".format(x1))
        area.add_line("{0}".format(y1)) 
        area.add_line(json.dumps({})) #meta line
        area.add_line("True") #is region
        area.add_line("{0}".format(x2)) #w/h ... but we're abusing it for a position
        area.add_line("{0}".format(y2)) 


