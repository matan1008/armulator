from armulator.opcodes.abstract_opcode import AbstractOpcode


class MsrImmediateApplication(AbstractOpcode):
    def __init__(self, write_nzcvq, write_g, imm32):
        super(MsrImmediateApplication, self).__init__()
        self.write_nzcvq = write_nzcvq
        self.write_g = write_g
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_nzcvq:
                processor.core_registers.set_cpsr_n(self.imm32[0])
                processor.core_registers.set_cpsr_z(self.imm32[1])
                processor.core_registers.set_cpsr_c(self.imm32[2])
                processor.core_registers.set_cpsr_v(self.imm32[3])
                processor.core_registers.set_cpsr_q(self.imm32[4])
            if self.write_g:
                processor.core_registers.set_cpsr_ge(self.imm32[12:16])
