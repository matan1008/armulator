from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.opcode import Opcode


class Ubfx(Opcode):
    def __init__(self, instruction, lsbit, widthminus1, d, n):
        super().__init__(instruction)
        self.lsbit = lsbit
        self.widthminus1 = widthminus1
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            msbit = self.lsbit + self.widthminus1
            if msbit <= 31:
                processor.registers.set(self.d, substring(processor.registers.get(self.n), msbit, self.lsbit))
            else:
                print('unpredictable')
