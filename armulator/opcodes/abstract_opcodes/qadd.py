from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat_q


class Qadd(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qadd, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result, sat = signed_sat_q(
                    processor.core_registers.get(self.m).int + processor.core_registers.get(self.n).int, 32)
            processor.core_registers.set(self.d, result)
            if sat:
                processor.core_registers.cpsr.set_q(True)
