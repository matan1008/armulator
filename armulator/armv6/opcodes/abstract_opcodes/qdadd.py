from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import signed_sat_q


class Qdadd(AbstractOpcode):
    def __init__(self, m, d, n):
        super(Qdadd, self).__init__()
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            doubled, sat1 = signed_sat_q(2 * processor.registers.get(self.n).int, 32)
            result, sat2 = signed_sat_q(processor.registers.get(self.m).int + doubled.int, 32)
            processor.registers.set(self.d, result)
            if sat1 or sat2:
                processor.registers.cpsr.set_q(True)
