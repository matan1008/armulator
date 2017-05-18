from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.configurations import ProcessorID


class Clrex(AbstractOpcode):
    def __init__(self):
        super(Clrex, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            processor.clear_exclusive_local(ProcessorID())
