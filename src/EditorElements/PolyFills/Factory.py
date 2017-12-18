import json
class Factory:
    def make_light( area, x, y, light_class ):
        area.add_line("OBJECT")
        area.add_line("light")
        area.add_line("{0}".format(x))
        area.add_line("{0}".format(y))
        area.add_line(json.dumps({"class":light_class}))
        area.add_line("True")
        area.add_line("0")
        area.add_line("0")
