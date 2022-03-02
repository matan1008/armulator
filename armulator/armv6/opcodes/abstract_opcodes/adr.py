from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align


class Adr(Opcode):
    def __init__(self, instruction, add, d, imm32):
        super().__init__(instruction)
        self.add = add
        self.d = d
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result = bits_add(align(processor.registers.get_pc(), 4), self.imm32, 32) if self.add else bits_sub(
                    align(processor.registers.get_pc(), 4), self.imm32, 32)
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
