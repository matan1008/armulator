from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import unsigned_sat_q, zero_extend


class Usat16(AbstractOpcode):
    def __init__(self, saturate_to, d, n):
        super(Usat16, self).__init__()
        self.saturate_to = saturate_to
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            result1, sat1 = unsigned_sat_q(processor.registers.get(self.n)[16:32].int, self.saturate_to)
            result2, sat2 = unsigned_sat_q(processor.registers.get(self.n)[0:16].int, self.saturate_to)
            processor.registers.set(self.d, zero_extend(result2, 16) + zero_extend(result1, 16))
            if sat1 or sat2:
                processor.registers.cpsr.set_q(True)
