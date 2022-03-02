from armulator.armv6.opcodes.opcode import Opcode


class CdpCdp2(Opcode):
    def __init__(self, instruction, cp):
        super().__init__(instruction)
        self.cp = cp

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                processor.coproc_internal_operation(self.cp, processor.this_instr())
