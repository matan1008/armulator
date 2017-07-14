from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import unsigned_sat_q, zero_extend


class Usat(AbstractOpcode):
    def __init__(self, saturate_to, d, n, shift_t, shift_n):
        super(Usat, self).__init__()
        self.saturate_to = saturate_to
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            operand = shift(processor.registers.get(self.n), self.shift_t, self.shift_n,
                            processor.registers.cpsr.get_c())
            result, sat = unsigned_sat_q(operand.int, self.saturate_to)
            processor.registers.set(self.d, zero_extend(result, 32))
            if sat:
                processor.registers.cpsr.set_q(True)
