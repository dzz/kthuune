class layer_map:
    key_order = [
                "all",
                "floor",
                "floor_decorators",
                "floor_interactions",
                "totem",
                "wall",
                "npc",
                "decorator"
            ]

    def get_layer_id(key):
        return layer_map.key_order.index(key)
