from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.enums import InstrSet


class Enterx(AbstractOpcode):
    def __init__(self, is_enterx):
        super(Enterx, self).__init__()
        self.is_enterx = is_enterx

    def execute(self, processor):
        if self.is_enterx:
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            else:
                processor.registers.select_instr_set(InstrSet.InstrSet_ThumbEE)
        else:
            processor.registers.select_instr_set(InstrSet.InstrSet_Thumb)
