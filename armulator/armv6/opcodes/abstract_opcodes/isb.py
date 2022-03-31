from armulator.armv6.opcodes.opcode import Opcode


class Isb(Opcode):
    def __init__(self, instruction):
        super().__init__(instruction)

    def execute(self, processor):
        if processor.condition_passed():
            processor.instruction_synchronization_barrier()
