from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode


class Cdp(AbstractOpcode):
    def __init__(self, cp):
        super(Cdp, self).__init__()
        self.cp = cp

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_internal_operation(self.cp, processor.this_instr())
