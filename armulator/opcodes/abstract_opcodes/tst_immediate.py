from armulator.opcodes.abstract_opcode import AbstractOpcode


class TstImmediate(AbstractOpcode):
    def __init__(self, n, imm32, carry):
        super(TstImmediate, self).__init__()
        self.n = n
        self.imm32 = imm32
        self.carry = carry

    def execute(self, processor):
        if processor.condition_passed():
            result = processor.core_registers.get(self.n) & self.imm32
            processor.core_registers.set_cpsr_n(result[0])
            processor.core_registers.set_cpsr_z(result.all(False))
            processor.core_registers.set_cpsr_c(self.carry)
