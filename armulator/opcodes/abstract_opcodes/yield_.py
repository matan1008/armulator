from armulator.opcodes.abstract_opcode import AbstractOpcode


class Yield(AbstractOpcode):
    def __init__(self):
        super(Yield, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            processor.hint_yield()
