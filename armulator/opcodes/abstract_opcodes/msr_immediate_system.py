from armulator.opcodes.abstract_opcode import AbstractOpcode


class MsrImmediateSystem(AbstractOpcode):
    def __init__(self, write_spsr, mask, imm32):
        super(MsrImmediateSystem, self).__init__()
        self.write_spsr = write_spsr
        self.mask = mask
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_spsr:
                processor.core_registers.spsr_write_by_instr(self.imm32, self.mask)
            else:
                processor.core_registers.cpsr_write_by_instr(self.imm32, self.mask, False)
                if (processor.core_registers.CPSR[27:32] == "0b11010" and
                        processor.core_registers.get_cpsr_j() == "1" and
                        processor.core_registers.get_cpsr_t() == "1"):
                    print "unpredictable"
