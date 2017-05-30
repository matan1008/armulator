from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add_with_carry


class AddImmediateThumb(AbstractOpcode):
    def __init__(self, setflags, d, n, imm32):
        super(AddImmediateThumb, self).__init__()
        self.setflags = setflags
        self.d = d
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.registers.get(self.n), self.imm32, "0")
            processor.registers.set(self.d, result)
            if self.setflags:
                processor.registers.cpsr.set_n(result[0])
                processor.registers.cpsr.set_z(result.all(0))
                processor.registers.cpsr.set_c(carry)
                processor.registers.cpsr.set_v(overflow)
