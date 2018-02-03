from Beagle import API as BGL

class BrushFile:
    sequence = None
    def get_filename(level_name):
        if not BrushFile.sequence:
            return BGL.environment.settings['app_dir'] + "resources/brush_levels/" + level_name + ".brushes"
        else:
            filename = "{0}/{1}.brushes".format(BGL.assets.get('KT-player/path/sequence'),BrushFile.sequence)
            return filename

    def save(Brushes):
        brush_file = open(BrushFile.get_filename(Brushes.level_name), "w")
        brush_file.write('BRUSH_HEADER\n')
        brush_file.write(Brushes.level_name + '\n')
        brush_file.write("{0}\n".format(int(Brushes.w_size)))
        for brush in Brushes.brushes:
            brush_file.write('BRUSH\n')
            brush_file.write('{0}\n'.format(brush.x1))
            brush_file.write('{0}\n'.format(brush.y1))
            brush_file.write('{0}\n'.format(brush.x2))
            brush_file.write('{0}\n'.format(brush.y2))
            brush_file.write('{0}\n'.format(brush.polyfill_key))

        brush_file.close()

    def load(Brushes):
        Brushes.next_id = 1
        Brushes.brushes = []
        brush_file = open(BrushFile.get_filename(Brushes.level_name))
        lines = brush_file.read().split('\n')
        brush = None
        row = 0
        mode = 'HEADER'
        for line in lines:
            if line == 'BRUSH':
                mode = 'BRUSH'
                if brush:
                    Brushes.brushes.append(brush)
                brush = Brushes.Brush()
                row = 0
            if mode == 'HEADER':
                if row == 2:
                    Brushes.w_size = float(line)
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
