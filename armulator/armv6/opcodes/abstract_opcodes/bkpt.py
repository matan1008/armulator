from armulator.armv6.opcodes.opcode import Opcode


class Bkpt(Opcode):
    def execute(self, processor):
        processor.bkpt_instr_debug_event()
