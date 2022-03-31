from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.decoders import arm_branch_branch_with_link_and_block_data_transfer
from armulator.armv6.opcodes.decoders import arm_coprocessor_instructions_and_supervisor_call
from armulator.armv6.opcodes.decoders import arm_data_processing_and_miscellaneous_instructions
from armulator.armv6.opcodes.decoders import arm_load_store_word_and_unsigned_byte
from armulator.armv6.opcodes.decoders import arm_media_instructions
from armulator.armv6.opcodes.decoders import arm_unconditional_instructions


def decode_instruction(instr):
    cond = substring(instr, 31, 28)
    op1 = substring(instr, 27, 25)
    instr_27_26 = substring(instr, 27, 26)
    op = bit_at(instr, 4)
    if cond != 0b1111 and instr_27_26 == 0b00:
        # Data-processing and miscellaneous instructions
        return arm_data_processing_and_miscellaneous_instructions.decode_instruction(instr)
    elif cond != 0b1111 and ((op1 == 0b010) or (op1 == 0b011 and not op)):
        # Load/store word and unsigned byte
        return arm_load_store_word_and_unsigned_byte.decode_instruction(instr)
    elif cond != 0b1111 and op1 == 0b011 and op:
        # Media instructions
        return arm_media_instructions.decode_instruction(instr)
    elif cond != 0b1111 and instr_27_26 == 0b10:
        # Branch, branch with link, and block data transfer
        return arm_branch_branch_with_link_and_block_data_transfer.decode_instruction(instr)
    elif cond != 0b1111 and instr_27_26 == 0b11:
        # Coprocessor instructions, and Supervisor Call
        return arm_coprocessor_instructions_and_supervisor_call.decode_instruction(instr)
    elif cond == 0b1111:
        # Unconditional instructions
        return arm_unconditional_instructions.decode_instruction(instr)
