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
            operand2 = (processor.core_registers.get(self.m)[0:16]
                        if self.m_high
                        else processor.core_registers.get(self.m)[16:])
            result = processor.core_registers.get(self.n).int * operand2.int + (
                processor.core_registers.get(self.a).int << 16)
            processor.core_registers.set(self.d, BitArray(int=result, length=48)[0:32])
            if (result >> 16) != processor.core_registers.get(self.d).int:
                processor.core_registers.set_cpsr_q(True)
