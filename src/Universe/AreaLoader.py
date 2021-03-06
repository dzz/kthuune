import json 

area_cache = {}
def get_area_data(data):
    global area_cache
    key = "".join(data)
    if key in area_cache:
        return area_cache[key]
    def defunge_line(line):
        #print(line)
        return [[line['x1'],line['y1']],[line['x2'],line['y2']]]

    parsed = {
        "width" : 100.0,
        "height" : 100.0,
        "light_occluders" : [],
        "physics_occluders" : [],
        "decorators" : [],
        "object_defs" : [],
        "prop_defs" : [],
        "magic_lines" : [],
        "tile_defs" : [],
        "tile_defs_fg" : []
    }

    data = data.replace("\r","").split("\n")

    lines = []

    mode = ""
    for txt in data:
        ########### read atom
        if txt=="MODEL":
            mode = txt
            row = 0
            continue
        if txt=="LINE":
            mode = txt
            row = 0
            lines.append({})
            continue
        if txt=="MAGIC_LINE":
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
        if txt=="TILE":
            mode = txt
            parsed["tile_defs"].append({})
            row = 0
            continue

        ##################### parse atom
        if mode == "MODEL":
            if row == 0:
                parsed["width"] = float(txt)
            if row == 1:
                parsed["height"] = float(txt)

        if mode in [ "LINE", "MAGIC_LINE" ]:
            l = lines[-1]
            if row == 0:
                lines[-1]["x1"] = float(txt)
            if row == 1:
                lines[-1]["y1"] = float(txt)
            if row == 2:
                lines[-1]["x2"] = float(txt)
            if row == 3:
                lines[-1]["y2"] = float(txt)

            if mode == "LINE":
                if row == 4:
                    if txt=="True":
                        parsed["light_occluders"].append(defunge_line(l))
                if row == 5:
                    if txt=="True":
                        parsed["physics_occluders"].append(defunge_line(l))
                if row == 6:
                    if txt=="True":
                        parsed["decorators"].append(defunge_line(l))
            if mode == "MAGIC_LINE":
                if row == 4:
                    parsed["magic_lines"].append( { "line" : l, "magic_number" : int(txt) })

        if mode == "OBJECT":
            o = parsed["object_defs"][-1]
            if row == 0:
                o["key"] = txt
            if row == 1:
                o["x"] = float(txt)
            if row == 2:
                o["y"] = float(txt)
            if row == 3:

                if o["key"] in [ "door_pin", "door_end", "door_sensor" ]:
                    o["meta"] = {}
                    o["meta"]["door"] = txt.replace("\r","").replace("\n","")
                elif o["key"] == "area_switch" and "=>" in txt:
                    txt = txt.replace("\r","").replace("\n","")
                    s = txt.split("=>")
                    o["meta"] = {}
                    o["meta"]["name"] = s[0]
                    o["meta"]["target_switch"] = s[1]
                    o["meta"]["target_area"]="self"
                else:
                    try:
                        o["meta"] = json.loads(txt)
                    except Exception as e:
                        o["meta"] = {}
            if row == 4:
                if(txt=="True"):
                    o["region"] = True
            if row == 5:
                o["w"] = float(txt)
            if row == 6:
                o["h"] = float(txt)

        if mode == "TILE":
            t = parsed["tile_defs"][-1]
            if row ==0:
                t["x"] = int(txt)
            if row ==1:
                t["y"] = int(txt) 
            if row ==2:
                t["idx"] = int(txt)
            if row ==3:
                t["layer"] = "fg"

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
            if row == 6:
                p["layer"] = float(txt)
                    
        row = row + 1


    for tile_def in parsed["tile_defs"]:
        tile_def["x"] = tile_def["x"] + int(parsed["width"]/2)
        tile_def["y"] = tile_def["y"] + int(parsed["width"]/2)

    area_cache[key] = parsed
    return parsed

#data = open('c:\\tmp\\test.area').read()
#print(get_area_data(data))

