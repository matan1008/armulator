from armulator.armv6.arm_exceptions import UndefinedInstructionException
import thumb_load_store_multiple
import thumb_load_store_dual_load_store_exclusive_table_branch
import thumb_data_processing_shifted_register
import thumb_coprocessor_advanced_simd_and_floating_point_instructions
import thumb_data_processing_modified_immediate
import thumb_data_processing_plain_binary_immediate
import thumb_branches_and_miscellaneous_control
import thumb_store_single_data_item
import thumb_load_byte_memory_hints
import thumb_load_halfword_memory_hints
import thumb_load_word
import thumb_data_processing_register
import thumb_multiply_multiply_accumulate_and_absolute_difference
import thumb_long_multiply_long_multiply_accumulate_and_divide


def decode_instruction(instr):
    if instr[3:5] == "0b01" and instr[5:7] == "0b00" and not instr[9]:
        # Load/store multiple
        return thumb_load_store_multiple.decode_instruction(instr)
    elif instr[3:5] == "0b01" and instr[5:7] == "0b00" and instr[9]:
        # Load/store dual, load/store exclusive, table branch
        return thumb_load_store_dual_load_store_exclusive_table_branch.decode_instruction(instr)
    elif instr[3:5] == "0b01" and instr[5:7] == "0b01":
        # Data-processing (shifted register)
        return thumb_data_processing_shifted_register.decode_instruction(instr)
    elif instr[3:5] == "0b01" and instr[5]:
        # Coprocessor, Advanced SIMD, and Floating-point instructions
        return thumb_coprocessor_advanced_simd_and_floating_point_instructions.decode_instruction(instr)
    elif instr[3:5] == "0b10" and not instr[6] and not instr[16]:
        # Data-processing (modified immediate)
        return thumb_data_processing_modified_immediate.decode_instruction(instr)
    elif instr[3:5] == "0b10" and instr[6] and not instr[16]:
        # Data-processing (plain binary immediate)
        return thumb_data_processing_plain_binary_immediate.decode_instruction(instr)
    elif instr[3:5] == "0b10" and instr[16]:
        # Branches and miscellaneous control
        return thumb_branches_and_miscellaneous_control.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:8] == "0b000" and not instr[11]:
        # Store single data item
        return thumb_store_single_data_item.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:7] == "0b00" and instr[9:12] == "0b001":
        # Load byte, memory hints
        return thumb_load_byte_memory_hints.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:7] == "0b00" and instr[9:12] == "0b011":
        # Load halfword, memory hints
        return thumb_load_halfword_memory_hints.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:7] == "0b00" and instr[9:12] == "0b101":
        # Load word
        return thumb_load_word.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:7] == "0b00" and instr[9:12] == "0b111":
        raise UndefinedInstructionException()
    elif instr[3:5] == "0b11" and instr[5:8] == "0b001" and not instr[11]:
        # Advanced SIMD element or structure load/store instructions
        # will not be implemented
        raise NotImplementedError()
    elif instr[3:5] == "0b11" and instr[5:8] == "0b010":
        # Data-processing (register)
        return thumb_data_processing_register.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:9] == "0b0110":
        # Multiply, multiply accumulate, and absolute difference
        return thumb_multiply_multiply_accumulate_and_absolute_difference.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5:9] == "0b0111":
        # Long multiply, long multiply accumulate, and divide
        return thumb_long_multiply_long_multiply_accumulate_and_divide.decode_instruction(instr)
    elif instr[3:5] == "0b11" and instr[5]:
        # Coprocessor, Advanced SIMD, and Floating-point instructions
        return thumb_coprocessor_advanced_simd_and_floating_point_instructions.decode_instruction(instr)
