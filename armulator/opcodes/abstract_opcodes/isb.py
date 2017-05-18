from armulator.opcodes.abstract_opcode import AbstractOpcode


class Isb(AbstractOpcode):
    def __init__(self):
        super(Isb, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            processor.instruction_synchronization_barrier()
