from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add as bits_add, sub as bits_sub, align


class PldLiteral(AbstractOpcode):
    def __init__(self, add, imm32):
        super(PldLiteral, self).__init__()
        self.add = add
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            address = bits_add(align(processor.core_registers.get_pc(), 4), self.imm32, 32) if self.add else bits_sub(
                    align(processor.core_registers.get_pc(), 4), self.imm32, 32)
            processor.hint_preload_data(address)
