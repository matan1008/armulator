from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.configurations import ArchVersion


class Mla(AbstractOpcode):
    def __init__(self, setflags, m, a, d, n):
        super(Mla, self).__init__()
        self.setflags = setflags
        self.m = m
        self.a = a
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = processor.registers.get(self.n).int
            operand2 = processor.registers.get(self.m).int
            addend = processor.registers.get(self.a).int
            result = operand1 * operand2 + addend
            f_result = BitArray(int=result, length=64)[32:]
            processor.registers.set(self.d, f_result)
            if self.setflags:
                processor.registers.cpsr.set_n(f_result[0])
                processor.registers.cpsr.set_z(not f_result.any(True))
                if ArchVersion() == 4:
                    processor.registers.cpsr.set_c(False)  # uknown
