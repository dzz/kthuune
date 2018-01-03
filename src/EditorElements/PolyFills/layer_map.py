class layer_map:
    key_order = [
                "all",
                "floor",
                "totem",
                "wall",
                "npc",
                "decorator"
            ]

    def get_layer_id(key):
        return layer_map.key_order.index(key)
