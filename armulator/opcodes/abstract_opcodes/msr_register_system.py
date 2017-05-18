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
                processor.core_registers.spsr_write_by_instr(processor.core_registers.get(self.n), self.mask)
            else:
                processor.core_registers.cpsr_write_by_instr(processor.core_registers.get(self.n), self.mask, False)
                if (processor.core_registers.get_cpsr_m() == "11010" and
                        processor.core_registers.get_cpsr_j() and processor.core_registers.get_cpsr_t()):
                    print "unpredictable"
