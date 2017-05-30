from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smlaw(AbstractOpcode):
    def __init__(self, m_high, m, a, d, n):
        super(Smlaw, self).__init__()
        self.m_high = m_high
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand2 = (processor.registers.get(self.m)[0:16]
                        if self.m_high
                        else processor.registers.get(self.m)[16:])
            result = processor.registers.get(self.n).int * operand2.int + (
                processor.registers.get(self.a).int << 16)
            processor.registers.set(self.d, BitArray(int=result, length=48)[0:32])
            if (result >> 16) != processor.registers.get(self.d).int:
                processor.registers.cpsr.set_q(True)
