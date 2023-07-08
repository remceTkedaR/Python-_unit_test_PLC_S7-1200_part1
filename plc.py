class PLC:
    def __init__(self):
        self.input_flags = {}
        self.output_flags = {}

    def read_input_flag(self, flag):
        return self.input_flags.get(flag, False)

    def write_output_flag(self, flag, value):
        self.output_flags[flag] = value

    def clear_output_flags(self):
        self.output_flags = {}