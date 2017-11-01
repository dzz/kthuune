class WorldMap:

    systems = {
        "Oort Cloud" : {
            "unlocked" : True,
            "destinations" : {
                "Crystaline Structure I." : { "unlocked" : True, "area_name" : "crystals1", "pin_name" : None }
            }
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

    
        
