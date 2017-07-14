from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.armv6.configurations import arch_version


class Umlal(AbstractOpcode):
    def __init__(self, setflags, m, d_hi, d_lo, n):
        super(Umlal, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.registers.get(self.n).uint * processor.registers.get(self.m).uint + (
                processor.registers.get(self.d_hi) + processor.registers.get(self.d_lo)).uint
            f_result = BitArray(uint=result, length=64)
            processor.registers.set(self.d_hi, f_result[0:32])
            processor.registers.set(self.d_lo, f_result[32:])
            if self.setflags:
                processor.registers.cpsr.set_n(f_result[0])
                processor.registers.cpsr.set_z(not f_result.any(True))
                if arch_version() == 4:
                    processor.registers.cpsr.set_c(False)  # unknown
                    processor.registers.cpsr.set_v(False)  # unknown
