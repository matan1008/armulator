from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import signed_sat_q


class Qdadd(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qdadd, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            doubled, sat1 = signed_sat_q(2 * processor.core_registers.get(self.n).int, 32)
            result, sat2 = signed_sat_q(processor.core_registers.get(self.m).int + doubled.int, 32)
            processor.core_registers.set(self.d, result)
            if sat1 or sat2:
                processor.core_registers.set_cpsr_q(True)
