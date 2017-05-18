from armulator.opcodes.abstract_opcode import AbstractOpcode


class Nop(AbstractOpcode):
    def __init__(self):
        super(Nop, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            pass
