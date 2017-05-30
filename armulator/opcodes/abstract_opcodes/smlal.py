from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.configurations import ArchVersion


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
            result = processor.core_registers.get(self.n).int * processor.core_registers.get(self.m).int + (
                processor.core_registers.get(self.d_hi) + processor.core_registers.get(self.d_lo)).int
            f_result = BitArray(int=result, length=64)
            processor.core_registers.set(self.d_hi, f_result[0:32])
            processor.core_registers.set(self.d_lo, f_result[32:])
            if self.setflags:
                processor.core_registers.cpsr.set_n(f_result[0])
                processor.core_registers.cpsr.set_z(not f_result.any(True))
                if ArchVersion() == 4:
                    processor.core_registers.cpsr.set_c(False)  # uknown
                    processor.core_registers.cpsr.set_v(False)  # uknown
