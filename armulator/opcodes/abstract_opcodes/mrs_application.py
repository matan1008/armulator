from armulator.opcodes.abstract_opcode import AbstractOpcode


class MrsApplication(AbstractOpcode):
    def __init__(self, d):
        super(MrsApplication, self).__init__()
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            processor.core_registers.set(self.d, processor.core_registers.get_cpsr_as_apsr())
