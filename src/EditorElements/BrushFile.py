from Beagle import API as BGL

class BrushFile:

    def get_folder():
        return BGL.environment.settings['app_dir'] + "resources/brush_levels/" 

    def get_filename(level_name):
        return BrushFile.get_folder() + level_name + ".brushes"

    def save(Brushes):
        brush_file = open(BrushFile.get_filename(Brushes.level_name), "w")
        brush_file.write('BRUSH_HEADER\n')
        brush_file.write(Brushes.level_name + '\n')
        for brush in Brushes.brushes:
            brush_file.write('BRUSH\n')
            brush_file.write('{0}\n'.format(brush.x1))
            brush_file.write('{0}\n'.format(brush.y1))
            brush_file.write('{0}\n'.format(brush.x2))
            brush_file.write('{0}\n'.format(brush.y2))
            brush_file.write('{0}\n'.format(brush.polyfill_key))

        brush_file.close()

    def load(Brushes, filename = None):
        Brushes.next_id = 1
        Brushes.brushes = []

        if filename is None:
            brush_file = open(BrushFile.get_filename(Brushes.level_name))
        else:
            brush_file = open(filename)

        lines = brush_file.read().split('\n')
        brush = None
        row = 0
        mode = 'HEADER'
        for line in lines:

            if line == 'HEADER':
                mode = 'HEADER'
                row = 0

            if line == 'BRUSH':
                mode = 'BRUSH'
                if brush:
                    Brushes.brushes.append(brush)
                brush = Brushes.Brush()
                row = 0

            if mode == 'HEADER':
                if row == 1:
                    Brushes.set_name(line)
            if mode == 'BRUSH':
                if row == 1:
                    brush.x1 = int(line)
                elif row == 2:
                    brush.y1 = int(line)
                elif row == 3:
                    brush.x2 = int(line)
                elif row == 4:
                    brush.y2 = int(line)
                elif row == 5:
                    brush.polyfill_key = line
            row+=1
        if brush:
            Brushes.brushes.append(brush)
        brush_file.close()
