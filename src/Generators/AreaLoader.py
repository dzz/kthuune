def get_area_data(data):

    def defunge_line(line):
        return [[line['x1'],line['y1']],[line['x2'],line['y2']]]

    parsed = {
        "width" : 100.0,
        "height" : 100.0,
        "light_occluders" : [],
        "physics_occluders" : [],
        "decorators" : [],
        "object_defs" : [],
        "prop_defs" : []
    }

    data = data.replace("\r","").split("\n")

    lines = []

    mode = ""
    for txt in data:
        if txt=="MODEL":
            mode = txt
            row = 0
            continue
        if txt=="LINE":
            mode = txt
            row = 0
            lines.append({})
            continue
        if txt=="OBJECT":
            mode = txt
            row = 0 
            parsed["object_defs"].append({})
            continue
        if txt=="PROP":
            mode = txt
            row = 0
            parsed["prop_defs"].append({})
            continue


        if mode == "MODEL":
            if row == 0:
                parsed["width"] = float(txt)
            if row == 1:
                parsed["height"] = float(txt)

        if mode == "LINE":
            l = lines[-1]
            if row == 0:
                lines[-1]["x1"] = float(txt)
            if row == 1:
                lines[-1]["y1"] = float(txt)
            if row == 2:
                lines[-1]["x2"] = float(txt)
            if row == 3:
                lines[-1]["y2"] = float(txt)

            if row == 4:
                if txt=="True":
                    parsed["light_occluders"].append(defunge_line(l))
            if row == 5:
                if txt=="True":
                    parsed["physics_occluders"].append(defunge_line(l))
            if row == 6:
                if txt=="True":
                    parsed["decorators"].append(defunge_line(l))

        if mode == "OBJECT":
            o = parsed["object_defs"][-1]
            if row == 0:
                o["key"] = txt
            if row == 1:
                o["x"] = float(txt)
            if row == 2:
                o["y"] = float(txt)
            if row == 3:
                try:
                    o["meta"] = json.loads(txt)
                except:
                    o["meta"] = {}

        if mode == "PROP":
            p = parsed["prop_defs"][-1]
            if row == 0:
                p["image"] = txt
            if row == 1:
                p["x"] = float(txt)
            if row == 2:
                p["y"] = float(txt)
            if row == 3:
                p["w"] = float(txt)
            if row == 4:
                p["h"] = float(txt)
            if row == 5:
                p["r"] = float(txt)
                    
        row = row + 1

    return parsed

#data = open('c:\\tmp\\test.area').read()
#print(get_area_data(data))

