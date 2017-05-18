from armulator.opcodes.abstract_opcode import AbstractOpcode


class Sev(AbstractOpcode):
    def __init__(self):
        super(Sev, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            processor.send_event()
