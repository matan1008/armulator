from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.shift import shift
from armulator.bits_ops import sign_extend, signed_sat_q


class Ssat(AbstractOpcode):
    def __init__(self, saturate_to, d, n, shift_t, shift_n):
        super(Ssat, self).__init__()
        self.saturate_to = saturate_to
        self.d = d
        self.n = n
        self.shift_t = shift_t
        self.shift_n = shift_n

    def execute(self, processor):
        if processor.condition_passed():
            operand = shift(processor.core_registers.get(self.n), self.shift_t, self.shift_n,
                            processor.core_registers.cpsr.get_c())
            result, sat = signed_sat_q(operand.int, self.saturate_to)
            processor.core_registers.set(self.d, sign_extend(result, 32))
            if sat:
                processor.core_registers.cpsr.set_q(True)
