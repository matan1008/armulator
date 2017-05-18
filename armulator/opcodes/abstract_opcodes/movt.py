from armulator.opcodes.abstract_opcode import AbstractOpcode


class Movt(AbstractOpcode):
    def __init__(self, d, imm16):
        super(Movt, self).__init__()
        self.d = d
        self.imm16 = imm16

    def execute(self, processor):
        if processor.condition_passed():
            processor.core_registers.set(self.d, self.imm16 + processor.core_registers.get(self.d)[16:32])
