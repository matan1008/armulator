from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.bits_ops import add_with_carry


class SubSpMinusImmediate(AbstractOpcode):
    def __init__(self, setflags, d, imm32):
        super(SubSpMinusImmediate, self).__init__()
        self.setflags = setflags
        self.d = d
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            result, carry, overflow = add_with_carry(processor.core_registers.get_sp(), ~self.imm32, "1")
            if self.d == 15:
                processor.alu_write_pc(result)
            else:
                processor.core_registers.set(self.d, result)
                if self.setflags:
                    processor.core_registers.set_cpsr_n(result[0])
                    processor.core_registers.set_cpsr_z(result.all(False))
                    processor.core_registers.set_cpsr_c(carry)
                    processor.core_registers.set_cpsr_v(overflow)
