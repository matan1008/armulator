from armulator.opcodes.abstract_opcode import AbstractOpcode


class Mcr(AbstractOpcode):
    def __init__(self, cp, t):
        super(Mcr, self).__init__()
        self.cp = cp
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_send_one_word(processor.registers.get(self.t), self.cp, processor.this_instr())
