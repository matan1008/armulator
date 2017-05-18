from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.configurations import ArchVersion


class Umull(AbstractOpcode):
    def __init__(self, setflags, m, d_hi, d_lo, n):
        super(Umull, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.n).uint * processor.core_registers.get(self.m).uint
            f_result = BitArray(uint=result, length=64)
            processor.core_registers.set(self.d_hi, f_result[0:32])
            processor.core_registers.set(self.d_lo, f_result[32:])
            if self.setflags:
                processor.core_registers.set_cpsr_n(f_result[0])
                processor.core_registers.set_cpsr_z(not f_result.any(True))
                if ArchVersion() == 4:
                    processor.core_registers.set_cpsr_c(False)  # unknown
                    processor.core_registers.set_cpsr_v(False)  # unknown
