from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add


class Cbz(AbstractOpcode):
    def __init__(self, nonzero, n, imm32):
        super(Cbz, self).__init__()
        self.nonzero = nonzero
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if self.nonzero != processor.core_registers.get(self.n).all(0):
            processor.branch_write_pc(add(processor.core_registers.get_pc(), self.imm32, 32))
