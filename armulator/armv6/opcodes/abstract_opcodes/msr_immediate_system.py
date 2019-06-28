from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class MsrImmediateSystem(AbstractOpcode):
    def __init__(self, write_spsr, mask, imm32):
        super(MsrImmediateSystem, self).__init__()
        self.write_spsr = write_spsr
        self.mask = mask
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_spsr:
                processor.registers.spsr_write_by_instr(self.imm32, self.mask)
            else:
                processor.registers.cpsr_write_by_instr(self.imm32, self.mask, False)
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and
                        processor.registers.cpsr.get_t()):
                    print("unpredictable")
