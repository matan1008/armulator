from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add_with_carry


class CmpImmediate(AbstractOpcode):
    def __init__(self, n, imm32):
        super(CmpImmediate, self).__init__()
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.registers.get(self.n), ~self.imm32, "1")
            processor.registers.cpsr.set_n(result[0])
            processor.registers.cpsr.set_z(result.all(False))
            processor.registers.cpsr.set_c(carry)
            processor.registers.cpsr.set_v(overflow)
