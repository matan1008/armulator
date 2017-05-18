from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import replicate


class Bfc(AbstractOpcode):
    def __init__(self, lsbit, msbit, d):
        super(Bfc, self).__init__()
        self.lsbit = lsbit
        self.msbit = msbit
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            if self.msbit >= self.lsbit:
                temp_rd = processor.core_registers.get(self.d)
                temp_rd[31 - self.msbit:32 - self.lsbit] = replicate("0", self.msbit - self.lsbit + 1)
                processor.core_registers.set(self.d, temp_rd)
            else:
                print "unpredictable"
