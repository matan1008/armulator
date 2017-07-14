from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class MrsApplication(AbstractOpcode):
    def __init__(self, d):
        super(MrsApplication, self).__init__()
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            processor.registers.set(self.d, processor.registers.cpsr.get_apsr())
