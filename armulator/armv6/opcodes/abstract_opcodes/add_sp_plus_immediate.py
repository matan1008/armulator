from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add_with_carry


class AddSpPlusImmediate(AbstractOpcode):
    def __init__(self, setflags, d, imm32):
        super(AddSpPlusImmediate, self).__init__()
        self.setflags = setflags
        self.d = d
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.registers.get_sp(), self.imm32, "0")
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.set_n(result[0])
                    processor.registers.cpsr.set_z(result.all(False))
                    processor.registers.cpsr.set_c(carry)
                    processor.registers.cpsr.set_v(overflow)
