from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.decoders import thumb_branches_and_miscellaneous_control
from armulator.armv6.opcodes.decoders import thumb_coprocessor_advanced_simd_and_floating_point_instructions
from armulator.armv6.opcodes.decoders import thumb_data_processing_modified_immediate
from armulator.armv6.opcodes.decoders import thumb_data_processing_plain_binary_immediate
from armulator.armv6.opcodes.decoders import thumb_data_processing_register
from armulator.armv6.opcodes.decoders import thumb_data_processing_shifted_register
from armulator.armv6.opcodes.decoders import thumb_load_byte_memory_hints
from armulator.armv6.opcodes.decoders import thumb_load_halfword_memory_hints
from armulator.armv6.opcodes.decoders import thumb_load_store_dual_load_store_exclusive_table_branch
from armulator.armv6.opcodes.decoders import thumb_load_store_multiple
from armulator.armv6.opcodes.decoders import thumb_load_word
from armulator.armv6.opcodes.decoders import thumb_long_multiply_long_multiply_accumulate_and_divide
from armulator.armv6.opcodes.decoders import thumb_multiply_multiply_accumulate_and_absolute_difference
from armulator.armv6.opcodes.decoders import thumb_store_single_data_item


def decode_instruction(instr):
    if substring(instr, 28, 27) == 0b01 and substring(instr, 26, 25) == 0b00 and not bit_at(instr, 22):
        # Load/store multiple
        return thumb_load_store_multiple.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b01 and substring(instr, 26, 25) == 0b00 and bit_at(instr, 22):
        # Load/store dual, load/store exclusive, table branch
        return thumb_load_store_dual_load_store_exclusive_table_branch.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b01 and substring(instr, 26, 25) == 0b01:
        # Data-processing (shifted register)
        return thumb_data_processing_shifted_register.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b01 and bit_at(instr, 26):
        # Coprocessor, Advanced SIMD, and Floating-point instructions
        return thumb_coprocessor_advanced_simd_and_floating_point_instructions.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b10 and not bit_at(instr, 25) and not bit_at(instr, 15):
        # Data-processing (modified immediate)
        return thumb_data_processing_modified_immediate.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b10 and bit_at(instr, 25) and not bit_at(instr, 15):
        # Data-processing (plain binary immediate)
        return thumb_data_processing_plain_binary_immediate.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b10 and bit_at(instr, 15):
        # Branches and miscellaneous control
        return thumb_branches_and_miscellaneous_control.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 24) == 0b000 and not bit_at(instr, 20):
        # Store single data item
        return thumb_store_single_data_item.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 25) == 0b00 and substring(instr, 22, 20) == 0b001:
        # Load byte, memory hints
        return thumb_load_byte_memory_hints.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 25) == 0b00 and substring(instr, 22, 20) == 0b011:
        # Load halfword, memory hints
        return thumb_load_halfword_memory_hints.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 25) == 0b00 and substring(instr, 22, 20) == 0b101:
        # Load word
        return thumb_load_word.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 25) == 0b00 and substring(instr, 22, 20) == 0b111:
        raise UndefinedInstructionException()
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 24) == 0b001 and not bit_at(instr, 20):
        # Advanced SIMD element or structure load/store instructions
        # will not be implemented
        raise NotImplementedError()
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 24) == 0b010:
        # Data-processing (register)
        return thumb_data_processing_register.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 23) == 0b0110:
        # Multiply, multiply accumulate, and absolute difference
        return thumb_multiply_multiply_accumulate_and_absolute_difference.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and substring(instr, 26, 23) == 0b0111:
        # Long multiply, long multiply accumulate, and divide
        return thumb_long_multiply_long_multiply_accumulate_and_divide.decode_instruction(instr)
    elif substring(instr, 28, 27) == 0b11 and bit_at(instr, 26):
        # Coprocessor, Advanced SIMD, and Floating-point instructions
        return thumb_coprocessor_advanced_simd_and_floating_point_instructions.decode_instruction(instr)
