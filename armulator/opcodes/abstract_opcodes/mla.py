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
            operand1 = processor.core_registers.get(self.n).int
            operand2 = processor.core_registers.get(self.m).int
            addend = processor.core_registers.get(self.a).int
            result = operand1 * operand2 + addend
            f_result = BitArray(int=result, length=64)[32:]
            processor.core_registers.set(self.d, f_result)
            if self.setflags:
                processor.core_registers.set_cpsr_n(f_result[0])
                processor.core_registers.set_cpsr_z(not f_result.any(True))
                if ArchVersion() == 4:
                    processor.core_registers.set_cpsr_c(False)  # uknown
