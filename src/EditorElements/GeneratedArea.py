class GeneratedArea:
    width = 0
    height = 0

    output_data = ""

    def add_line(line):
        GeneratedArea.output_data = "{0}{1}\n".format(GeneratedArea.output_data,line)
        
    def serialize_model():
        GeneratedArea.add_line("MODEL")
        GeneratedArea.add_line("{0}".format(GeneratedArea.width))
        GeneratedArea.add_line("{0}".format(GeneratedArea.height))

    def serialize():
        GeneratedArea.output_data = ""
        GeneratedArea.serialize_model()

