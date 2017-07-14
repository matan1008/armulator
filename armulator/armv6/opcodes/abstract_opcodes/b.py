from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add


class B(AbstractOpcode):
    def __init__(self, imm32):
        super(B, self).__init__()
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            processor.branch_write_pc(add(processor.registers.get_pc(), self.imm32, 32))
