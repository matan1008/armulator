from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.armv6.configurations import arch_version


class Smlal(AbstractOpcode):
    def __init__(self, setflags, m, d_hi, d_lo, n):
        super(Smlal, self).__init__()
        self.setflags = setflags
        self.m = m
        self.d_hi = d_hi
        self.d_lo = d_lo
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.registers.get(self.n).int * processor.registers.get(self.m).int + (
                processor.registers.get(self.d_hi) + processor.registers.get(self.d_lo)).int
            f_result = BitArray(int=result, length=64)
            processor.registers.set(self.d_hi, f_result[0:32])
            processor.registers.set(self.d_lo, f_result[32:])
            if self.setflags:
                processor.registers.cpsr.set_n(f_result[0])
                processor.registers.cpsr.set_z(not f_result.any(True))
                if arch_version() == 4:
                    processor.registers.cpsr.set_c(False)  # uknown
                    processor.registers.cpsr.set_v(False)  # uknown
