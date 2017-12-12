from Newfoundland.Object import Object

class Door(Object):
    def customize(self):
        self.visible = False
        self.tick_type = Object.TickTypes.TICK_FOREVER
        self.parsed_pin = [ self.door_pin['x'], self.door_pin['y'] ]
        self.parsed_end = [ self.door_end['x'], self.door_end['y'] ]
        self.parsed_sensors = []
        for sensor in self.sensors:
            self.parsed_sensors.append([sensor['x'],sensor['y']])
        self.opening = False
        self.closed_ratio = 1.0
        self.effective_closed_ratio = 1.0
        self.sensrad2 = 30
        self.open_speed = 0.06
        self.close_speed = 0.1
    
    def tick(self):
        self.effective_closed_ratio = (self.effective_closed_ratio * 0.8) + (self.closed_ratio*0.2)
        self.opening = False
        for sensor in self.parsed_sensors:
            dx = self.floor.player.p[0] - sensor[0]
            dy = self.floor.player.p[1] - sensor[1]
            md = (dx*dx) + (dy*dy)
            if( md < self.sensrad2 ):
                self.opening = True
                break
        if self.opening:
            if self.closed_ratio > 0.0:
                self.closed_ratio = self.closed_ratio - self.open_speed                
        else:
            if self.closed_ratio < 1.0:
                self.closed_ratio = self.closed_ratio + self.close_speed

    def get_light_occluders(self):
        dx = (self.parsed_end[0] - self.parsed_pin[0]) * self.effective_closed_ratio
        dy = (self.parsed_end[1] - self.parsed_pin[1]) * self.effective_closed_ratio
       
        ex = dx + self.parsed_pin[0] 
        ey = dy + self.parsed_pin[1] 

        return [ [ self.parsed_pin, [ex,ey] ] ]
