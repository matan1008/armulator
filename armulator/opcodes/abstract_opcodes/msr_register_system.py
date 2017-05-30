from armulator.opcodes.abstract_opcode import AbstractOpcode


class MsrRegisterSystem(AbstractOpcode):
    def __init__(self, write_spsr, mask, n):
        super(MsrRegisterSystem, self).__init__()
        self.write_spsr = write_spsr
        self.mask = mask
        self.n = n

    def execute(self, processor):
        if processor.condition_passed():
            if self.write_spsr:
                processor.registers.spsr_write_by_instr(processor.registers.get(self.n), self.mask)
            else:
                processor.registers.cpsr_write_by_instr(processor.registers.get(self.n), self.mask, False)
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and processor.registers.cpsr.get_t()):
                    print "unpredictable"
