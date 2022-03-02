from armulator.armv6.bits_ops import to_signed, to_unsigned, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.opcode import Opcode


class Mul(Opcode):
    def __init__(self, instruction, setflags, m, d, n):
        super().__init__(instruction)
        self.setflags = setflags
        self.m = m
        self.d = d
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            operand1 = to_signed(processor.registers.get(self.n), 32)
            operand2 = to_signed(processor.registers.get(self.m), 32)
            result = operand1 * operand2
            f_result = to_unsigned(result, 32)
            processor.registers.set(self.d, f_result)
            if self.setflags:
                processor.registers.cpsr.n = bit_at(result, 31)
                processor.registers.cpsr.z = 0 if result else 1
                if arch_version() == 4:
                    processor.registers.cpsr.c = 0  # unknown
