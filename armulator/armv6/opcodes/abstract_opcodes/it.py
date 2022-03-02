from armulator.armv6.bits_ops import chain
from armulator.armv6.opcodes.opcode import Opcode


class It(Opcode):
    def __init__(self, instruction, firstcond, mask):
        super().__init__(instruction)
        self.firstcond = firstcond
        self.mask = mask

    def execute(self, processor):
        processor.registers.cpsr.it = chain(self.firstcond, self.mask, 4)
