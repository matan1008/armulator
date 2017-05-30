from armulator.opcodes.abstract_opcode import AbstractOpcode


class Mrs(AbstractOpcode):
    def __init__(self, read_spsr, d):
        super(Mrs, self).__init__()
        self.read_spsr = read_spsr
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            if self.read_spsr:
                if processor.registers.current_mode_is_user_or_system():
                    print "unpredictable"
                else:
                    processor.registers.set(self.d, processor.registers.get_spsr())
            else:
                processor.registers.set(self.d, processor.registers.cpsr.value & "0xF8FF03DF")
                if not processor.registers.current_mode_is_not_user():
                    temp_register = processor.registers.get(self.d)
                    temp_register[-5:] = 0
                    temp_register[22:26] = 0
                    processor.registers.set(self.d, temp_register)
