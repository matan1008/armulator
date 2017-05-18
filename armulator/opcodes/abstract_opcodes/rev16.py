from armulator.opcodes.abstract_opcode import AbstractOpcode


class Rev16(AbstractOpcode):
    def __init__(self, m, d):
        super(Rev16, self).__init__()
        self.m = m
        self.d = d

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.m)[8:16]
            result += processor.core_registers.get(self.m)[0:8]
            result += processor.core_registers.get(self.m)[24:32]
            result += processor.core_registers.get(self.m)[16:24]
            processor.core_registers.set(self.d, result)
