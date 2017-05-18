from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import UndefinedInstructionException
from armulator.enums import InstrSet


class Enterx(AbstractOpcode):
    def __init__(self, is_enterx):
        super(Enterx, self).__init__()
        self.is_enterx = is_enterx

    def execute(self, processor):
        if self.is_enterx:
            if processor.core_registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            else:
                processor.core_registers.select_instr_set(InstrSet.InstrSet_ThumbEE)
        else:
            processor.core_registers.select_instr_set(InstrSet.InstrSet_Thumb)
