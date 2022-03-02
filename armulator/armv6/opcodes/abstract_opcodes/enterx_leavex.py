from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.enums import InstrSet


class EnterxLeavex(Opcode):
    def __init__(self, instruction, is_enterx):
        super().__init__(instruction)
        self.is_enterx = is_enterx

    def execute(self, processor):
        if self.is_enterx:
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            else:
                processor.registers.select_instr_set(InstrSet.THUMB_EE)
        else:
            processor.registers.select_instr_set(InstrSet.THUMB)
