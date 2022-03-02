from armulator.armv6.bits_ops import set_substring
from armulator.armv6.opcodes.opcode import Opcode


class Bfc(Opcode):
    def __init__(self, instruction, lsbit, msbit, d):
        super().__init__(instruction)
        self.lsbit = lsbit
        self.msbit = msbit
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            if self.msbit >= self.lsbit:
                temp_rd = processor.registers.get(self.d)
                processor.registers.set(self.d, set_substring(temp_rd, self.msbit, self.lsbit, 0))
            else:
                print('unpredictable')
