from armulator.opcodes.abstract_opcode import AbstractOpcode


class Mcrr(AbstractOpcode):
    def __init__(self, cp, t, t2):
        super(Mcrr, self).__init__()
        self.cp = cp
        self.t = t
        self.t2 = t2

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_send_two_words(processor.core_registers.get(self.t2),
                                                processor.core_registers.get(self.t), self.cp,
                                                processor.this_instr())
