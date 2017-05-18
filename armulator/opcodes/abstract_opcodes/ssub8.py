from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Ssub8(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Ssub8, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            diff1 = processor.core_registers.get(self.n)[24:32].int - processor.core_registers.get(self.m)[24:32].int
            diff2 = processor.core_registers.get(self.n)[16:24].int - processor.core_registers.get(self.m)[16:24].int
            diff3 = processor.core_registers.get(self.n)[8:16].int - processor.core_registers.get(self.m)[8:16].int
            diff4 = processor.core_registers.get(self.n)[0:8].int - processor.core_registers.get(self.m)[0:8].int
            processor.core_registers.set(self.d,
                                         BitArray(int=diff4, length=8) + BitArray(int=diff3, length=8) + BitArray(
                                             int=diff2, length=8) + BitArray(int=diff1, length=8))
            ge = "0b"
            ge += "1" if diff4 >= 0 else "0"
            ge += "1" if diff3 >= 0 else "0"
            ge += "1" if diff2 >= 0 else "0"
            ge += "1" if diff1 >= 0 else "0"
            processor.core_registers.set_cpsr_ge(ge)
