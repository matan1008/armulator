from armulator.armv6.bits_ops import add
from armulator.armv6.opcodes.opcode import Opcode


class Cbz(Opcode):
    def __init__(self, instruction, nonzero, n, imm32):
        super().__init__(instruction)
        self.nonzero = nonzero
        self.n = n
        self.imm32 = imm32

    def execute(self, processor):
        if self.nonzero ^ (int(processor.registers.get(self.n) == 0)):
            processor.branch_write_pc(add(processor.registers.get_pc(), self.imm32, 32))
