from armulator.opcodes.abstract_opcode import AbstractOpcode


class Bx(AbstractOpcode):
    def __init__(self, m):
        super(Bx, self).__init__()
        self.m = m

    def execute(self, processor):
        if processor.condition_passed():
            processor.bx_write_pc(processor.registers.get(self.m))
