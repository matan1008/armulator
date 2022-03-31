from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.opcode import Opcode


class MrcMrc2(Opcode):
    def __init__(self, instruction, cp, t):
        super().__init__(instruction)
        self.cp = cp
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                value = processor.coproc_get_one_word(self.cp, processor.this_instr())
                if self.t != 15:
                    processor.registers.set(self.t, value)
                else:
                    processor.registers.cpsr.n = bit_at(value, 31)
                    processor.registers.cpsr.z = bit_at(value, 30)
                    processor.registers.cpsr.c = bit_at(value, 29)
                    processor.registers.cpsr.v = bit_at(value, 28)
