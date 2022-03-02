from armulator.armv6.opcodes.opcode import Opcode


class Clz(Opcode):
    def __init__(self, instruction, m, d):
        super().__init__(instruction)
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            processor.registers.set(self.d, 32 - processor.registers.get(self.m).bit_length())
