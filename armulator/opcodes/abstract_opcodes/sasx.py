from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Sasx(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Sasx, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff = processor.core_registers.get(self.n)[16:32].int - processor.core_registers.get(self.m)[0:16].int
            sum_ = processor.core_registers.get(self.n)[0:16].int + processor.core_registers.get(self.m)[16:32].int
            processor.core_registers.set(self.d, BitArray(int=sum_, length=16) + BitArray(int=diff, length=16))
            ge = "0b"
            ge += "11" if sum_ >= 0 else "00"
            ge += "11" if diff >= 0 else "00"
            processor.core_registers.set_cpsr_ge(ge)
