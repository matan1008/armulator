from armulator.armv6.bits_ops import set_bit_at, set_substring
from armulator.armv6.opcodes.opcode import Opcode


class CpsThumb(Opcode):
    def __init__(self, instruction, affect_a, affect_i, affect_f, enable, disable, change_mode, mode=0b00000):
        super().__init__(instruction)
        self.affect_a = affect_a
        self.affect_i = affect_i
        self.affect_f = affect_f
        self.enable = enable
        self.disable = disable
        self.change_mode = change_mode
        self.mode = mode

    def execute(self, processor):
        if processor.registers.current_mode_is_not_user():
            cpsr_val = processor.registers.cpsr.value
            if self.enable:
                if self.affect_a:
                    cpsr_val = set_bit_at(cpsr_val, 8, 0)
                if self.affect_i:
                    cpsr_val = set_bit_at(cpsr_val, 7, 0)
                if self.affect_f:
                    cpsr_val = set_bit_at(cpsr_val, 6, 0)
            if self.disable:
                if self.affect_a:
                    cpsr_val = set_bit_at(cpsr_val, 8, 1)
                if self.affect_i:
                    cpsr_val = set_bit_at(cpsr_val, 7, 1)
                if self.affect_f:
                    cpsr_val = set_bit_at(cpsr_val, 6, 1)
            if self.change_mode:
                cpsr_val = set_substring(cpsr_val, 4, 0, self.mode)
            processor.registers.cpsr_write_by_instr(cpsr_val, 0b1111, False)
            if processor.registers.cpsr.m == 0b11010 and processor.registers.cpsr.j and processor.registers.cpsr.t:
                print('unpredictable')
