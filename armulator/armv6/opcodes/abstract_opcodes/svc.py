from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class Svc(AbstractOpcode):
    def __init__(self, imm32):
        super(Svc, self).__init__()
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            processor.call_supervisor(self.imm32[16:32])
