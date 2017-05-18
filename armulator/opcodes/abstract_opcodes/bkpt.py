from armulator.opcodes.abstract_opcode import AbstractOpcode


class Bkpt(AbstractOpcode):
    def __init__(self):
        super(Bkpt, self).__init__()

    def execute(self, processor):
        raise NotImplementedError()
