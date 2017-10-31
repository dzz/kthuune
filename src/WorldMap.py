class WorldMap:

    systems = {
        "Oort Cloud" : {
            "unlocked" : True,
            "destinations" : {
                "Crystaline Structure I." : { "unlocked" : True }
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

    
        
