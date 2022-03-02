from armulator.armv6.opcodes.opcode import Opcode


class McrMcr2(Opcode):
    def __init__(self, instruction, cp, t):
        super().__init__(instruction)
        self.cp = cp
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_send_one_word(processor.registers.get(self.t), self.cp, processor.this_instr())
