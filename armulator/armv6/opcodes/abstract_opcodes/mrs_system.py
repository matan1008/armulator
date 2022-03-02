from armulator.armv6.bits_ops import set_substring
from armulator.armv6.opcodes.opcode import Opcode


class MrsSystem(Opcode):
    def __init__(self, instruction, read_spsr, d):
        super().__init__(instruction)
        self.read_spsr = read_spsr
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            if self.read_spsr:
                if processor.registers.current_mode_is_user_or_system():
                    print('unpredictable')
                else:
                    processor.registers.set(self.d, processor.registers.get_spsr())
            else:
                processor.registers.set(self.d, processor.registers.cpsr.value & 0b11111000111111110000001111011111)
                if not processor.registers.current_mode_is_not_user():
                    temp_register = processor.registers.get(self.d)
                    temp_register = set_substring(temp_register, 4, 0, 0)  # unknown
                    temp_register = set_substring(temp_register, 9, 6, 0)  # unknown
                    processor.registers.set(self.d, temp_register)
