from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Uadd16(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Uadd16, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.registers.get(self.n)[16:32].uint + processor.registers.get(self.m)[16:32].uint
            sum2 = processor.registers.get(self.n)[0:16].uint + processor.registers.get(self.m)[0:16].uint
            processor.registers.set(self.d, BitArray(int=sum2, length=16) + BitArray(int=sum1, length=16))
            ge = "0b"
            ge += "11" if sum2 >= 0x10000 else "00"
            ge += "11" if sum1 >= 0x10000 else "00"
            processor.registers.cpsr.set_ge(ge)
