from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add_with_carry


class CmpImmediate(AbstractOpcode):
    def __init__(self, n, imm32):
        super(CmpImmediate, self).__init__()
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.core_registers.get(self.n), ~self.imm32, "1")
            processor.core_registers.cpsr.set_n(result[0])
            processor.core_registers.cpsr.set_z(result.all(False))
            processor.core_registers.cpsr.set_c(carry)
            processor.core_registers.cpsr.set_v(overflow)
