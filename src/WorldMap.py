class WorldMap:

    systems = {
        "Oort Cloud" : {
            "unlocked" : True,
            "destinations" : {
                "Unknown Origins" : { "unlocked" : True, "area_name" : "lacuna_canal", "pin_name" : None },
                "Crystal Formation" : { "unlocked" : True, "area_name" : "crystals1", "pin_name" : None },
                "The Gauntlet" : { "unlocked" : False, "area_name" : "doortest", "pin_name" : None },
                "Docks" : { "unlocked" : False, "area_name" : "docks", "pin_name" : None },
                "Grey World" : { "unlocked" : False, "area_name" : "grey_world", "pin_name" : None },
                "The Xeoliex" : { "unlocked" : False, "area_name" : "ship", "pin_name" : None },
            }
        },
        "Saisei II" : {
            "unlocked" : True,
            "destinations" : { }
        }
    }

    def get_available_systems():
        ret = []
        for key in WorldMap.systems:
            if WorldMap.systems[key]["unlocked"]:
                ret.append( key )
        return ret
            
    def get_available_destinations(system):
        ret = []
        for key in WorldMap.systems[system]["destinations"]:
            if WorldMap.systems[system]["destinations"][key]["unlocked"]:
                ret.append(key)
        return ret

    
        
