from armulator.opcodes.abstract_opcode import AbstractOpcode


class Bfi(AbstractOpcode):
    def __init__(self, lsbit, msbit, d, n):
        super(Bfi, self).__init__()
        self.lsbit = lsbit
        self.msbit = msbit
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if self.msbit >= self.lsbit:
                temp_rd = processor.registers.get(self.d)
                temp_rd[31 - self.msbit:32 - self.lsbit] = processor.registers.get(self.n)[
                                                           31 - self.msbit + self.lsbit:32]
                processor.registers.set(self.d, temp_rd)
            else:
                print "unpredictable"
