from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.configurations import processor_id


class Clrex(AbstractOpcode):
    def __init__(self):
        super(Clrex, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            processor.clear_exclusive_local(processor_id())
