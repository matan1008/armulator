from __future__ import absolute_import
from . import arm_instruction_set
from . import thumb_instruction_set
from armulator.armv6.enums import InstrSet


def decode_instruction(instr, processor):
    if processor.registers.current_instr_set() == InstrSet.InstrSet_ARM:
        # ARM instruction set encoding
        return arm_instruction_set.decode_instruction(instr, processor)
    elif processor.registers.current_instr_set() == InstrSet.InstrSet_Thumb:
        # Thumb instruction set encoding
        return thumb_instruction_set.decode_instruction(instr)