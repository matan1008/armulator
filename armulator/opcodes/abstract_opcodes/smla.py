from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray


class Smla(AbstractOpcode):
    def __init__(self, m_high, n_high, m, a, d, n):
        super(Smla, self).__init__()
        self.m_high = m_high
        self.n_high = n_high
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = processor.registers.get(self.n)[0:16] if self.n_high else processor.registers.get(
                    self.n)[16:]
            operand2 = processor.registers.get(self.m)[0:16] if self.m_high else processor.registers.get(
                    self.m)[16:]
            result = operand1.int * operand2.int + processor.registers.get(self.a).int
            processor.registers.set(self.d, BitArray(int=result, length=32))
            if result != BitArray(int=result, length=32).int:
                processor.registers.cpsr.set_q(True)
