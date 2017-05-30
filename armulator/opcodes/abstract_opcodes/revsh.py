from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import sign_extend


class Revsh(AbstractOpcode):
    def __init__(self, m, d):
        super(Revsh, self).__init__()
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = sign_extend(processor.registers.get(self.m)[24:32], 24)
            result += processor.registers.get(self.m)[16:24]
            processor.registers.set(self.d, result)
