from armulator.opcodes.abstract_opcode import AbstractOpcode


class Mrc(AbstractOpcode):
    def __init__(self, cp, t):
        super(Mrc, self).__init__()
        self.cp = cp
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                value = processor.coproc_get_one_word(self.cp, processor.this_instr())
                if self.t != 15:
                    processor.core_registers.set(self.t, value)
                else:
                    processor.core_registers.set_cpsr_n(value[0])
                    processor.core_registers.set_cpsr_z(value[1])
                    processor.core_registers.set_cpsr_c(value[2])
                    processor.core_registers.set_cpsr_v(value[3])
