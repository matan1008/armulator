from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Sadd8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Sadd8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            sum1 = processor.core_registers.get(self.n)[24:32].int + processor.core_registers.get(self.m)[24:32].int
            sum2 = processor.core_registers.get(self.n)[16:24].int + processor.core_registers.get(self.m)[16:24].int
            sum3 = processor.core_registers.get(self.n)[8:16].int + processor.core_registers.get(self.m)[8:16].int
            sum4 = processor.core_registers.get(self.n)[0:8].int + processor.core_registers.get(self.m)[0:8].int
            processor.core_registers.set(self.d, BitArray(int=sum4, length=8) + BitArray(int=sum3, length=8) + BitArray(
                    int=sum2, length=8) + BitArray(int=sum1, length=8))
            ge = "0b"
            ge += "1" if sum4 >= 0 else "0"
            ge += "1" if sum3 >= 0 else "0"
            ge += "1" if sum2 >= 0 else "0"
            ge += "1" if sum1 >= 0 else "0"
            processor.core_registers.cpsr.set_ge(ge)
