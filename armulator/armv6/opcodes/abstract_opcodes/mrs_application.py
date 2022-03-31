from armulator.armv6.opcodes.opcode import Opcode


class MrsApplication(Opcode):
    def __init__(self, instruction, d):
        super().__init__(instruction)
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            processor.registers.set(self.d, processor.registers.cpsr.apsr)
