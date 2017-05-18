from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add_with_carry


class CmnImmediate(AbstractOpcode):
    def __init__(self, n, imm32):
        super(CmnImmediate, self).__init__()
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.core_registers.get(self.n), self.imm32, "0")
            processor.core_registers.set_cpsr_n(result[0])
            processor.core_registers.set_cpsr_z(result.all(False))
            processor.core_registers.set_cpsr_c(carry)
            processor.core_registers.set_cpsr_v(overflow)
