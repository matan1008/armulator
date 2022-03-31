from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align
from armulator.armv6.opcodes.opcode import Opcode


class PldLiteral(Opcode):
    def __init__(self, instruction, add, imm32):
        super().__init__(instruction)
        self.add = add
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            address = bits_add(align(processor.registers.get_pc(), 4), self.imm32, 32) if self.add else bits_sub(
                align(processor.registers.get_pc(), 4), self.imm32, 32)
            processor.hint_preload_data(address)
