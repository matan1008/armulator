from armulator.armv6.opcodes.opcode import Opcode


class McrrMcrr2(Opcode):
    def __init__(self, instruction, cp, t, t2):
        super().__init__(instruction)
        self.cp = cp
        self.t = t
        self.t2 = t2

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_send_two_words(processor.registers.get(self.t2),
                                                processor.registers.get(self.t), self.cp,
                                                processor.this_instr())
