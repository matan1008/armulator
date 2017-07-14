import arm_data_processing_and_miscellaneous_instructions
import arm_load_store_word_and_unsigned_byte
import arm_media_instructions
import arm_branch_branch_with_link_and_block_data_transfer
import arm_coprocessor_instructions_and_supervisor_call
import arm_unconditional_instructions


def decode_instruction(instr, processor):
    if processor.current_cond().bin != "1111" and instr.bin[4:6] == "00":
        # Data-processing and miscellaneous instructions
        return arm_data_processing_and_miscellaneous_instructions.decode_instruction(instr)
    elif processor.current_cond().bin != "1111" and (
                (instr[4:7] == "0b010") or (instr[4:7] == "0b011" and not instr[27])):
        # Load/store word and unsigned byte
        return arm_load_store_word_and_unsigned_byte.decode_instruction(instr)
    elif processor.current_cond().bin != "1111" and instr[4:7] == "0b011" and instr[27]:
        # Media instructions
        return arm_media_instructions.decode_instruction(instr)
    elif processor.current_cond().bin != "1111" and instr.bin[4:6] == "10":
        # Branch, branch with link, and block data transfer
        return arm_branch_branch_with_link_and_block_data_transfer.decode_instruction(instr)
    elif processor.current_cond().bin != "1111" and instr.bin[4:6] == "11":
        # Coprocessor instructions, and Supervisor Call
        return arm_coprocessor_instructions_and_supervisor_call.decode_instruction(instr)
    elif processor.current_cond() == "0b1111":
        # Unconditional instructions
        return arm_unconditional_instructions.decode_instruction(instr)
