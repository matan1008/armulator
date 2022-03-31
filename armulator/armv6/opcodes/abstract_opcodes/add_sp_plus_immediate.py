from armulator.armv6.bits_ops import add_with_carry, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class AddSpPlusImmediate(Opcode):
    def __init__(self, instruction, setflags, d, imm32):
        super().__init__(instruction)
        self.setflags = setflags
        self.d = d
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.registers.get_sp(), self.imm32, 0)
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.n = bit_at(result, 31)
                    processor.registers.cpsr.z = 0 if result else 1
                    processor.registers.cpsr.c = carry
                    processor.registers.cpsr.v = overflow
