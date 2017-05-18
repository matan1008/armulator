from armulator.opcodes.abstract_opcode import AbstractOpcode


class MovImmediate(AbstractOpcode):
    def __init__(self, setflags, d, imm32, carry=""):
        super(MovImmediate, self).__init__()
        self.setflags = setflags
        self.d = d
        self.imm32 = imm32
        self.carry = carry

    def execute(self, processor):
        if processor.condition_passed():
            result = self.imm32
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.core_registers.set(self.d, result)
                if self.setflags:
                    processor.core_registers.set_cpsr_n(result[0])
                    processor.core_registers.set_cpsr_z(result.all(False))
                    processor.core_registers.set_cpsr_c(self.carry)
