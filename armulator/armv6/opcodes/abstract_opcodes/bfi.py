from armulator.armv6.bits_ops import set_substring, substring
from armulator.armv6.opcodes.opcode import Opcode


class Bfi(Opcode):
    def __init__(self, instruction, lsbit, msbit, d, n):
        super().__init__(instruction)
        self.lsbit = lsbit
        self.msbit = msbit
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if self.msbit >= self.lsbit:
                temp_rd = processor.registers.get(self.d)
                temp_rd = set_substring(temp_rd, self.msbit, self.lsbit,
                                        substring(processor.registers.get(self.n), self.msbit, self.lsbit))
                processor.registers.set(self.d, temp_rd)
            else:
                print('unpredictable')
