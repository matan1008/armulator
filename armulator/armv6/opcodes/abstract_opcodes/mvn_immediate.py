from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class MvnImmediate(AbstractOpcode):
    def __init__(self, setflags, d, imm32, carry):
        super(MvnImmediate, self).__init__()
        self.setflags = setflags
        self.d = d
        self.imm32 = imm32
        self.carry = carry

    def execute(self, processor):
        if processor.condition_passed():
            result = ~self.imm32
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.registers.set(self.d, result)
                if self.setflags:
                    processor.registers.cpsr.set_n(result[0])
                    processor.registers.cpsr.set_z(result.all(False))
                    processor.registers.cpsr.set_c(self.carry)
