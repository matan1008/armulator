from armulator.armv6.opcodes.opcode import Opcode


class Bx(Opcode):
    def __init__(self, instruction, m):
        super().__init__(instruction)
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            processor.bx_write_pc(processor.registers.get(self.m))
