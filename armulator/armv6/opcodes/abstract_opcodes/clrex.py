from armulator.armv6.configurations import processor_id
from armulator.armv6.opcodes.opcode import Opcode


class Clrex(Opcode):
    def __init__(self, instruction):
        super().__init__(instruction)

    def execute(self, processor):
        if processor.condition_passed():
            processor.clear_exclusive_local(processor_id())
