from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.decoders import arm_instruction_set
from armulator.armv6.opcodes.decoders import thumb_instruction_set


def decode_instruction(instr, processor):
    if processor.registers.current_instr_set() == InstrSet.ARM:
        # ARM instruction set encoding
        return arm_instruction_set.decode_instruction(instr)
    elif processor.registers.current_instr_set() == InstrSet.THUMB:
        # Thumb instruction set encoding
        return thumb_instruction_set.decode_instruction(instr, processor)
