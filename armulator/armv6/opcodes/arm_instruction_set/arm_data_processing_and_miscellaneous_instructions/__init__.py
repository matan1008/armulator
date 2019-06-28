from __future__ import absolute_import
from . import arm_data_processing_register
from . import arm_data_processing_register_shifted_register
from . import arm_miscellaneous_instructions
from . import arm_halfword_multiply_and_multiply_accumulate
from . import arm_multiply_and_multiply_accumulate
from . import arm_synchronization_primitives
from . import arm_extra_load_store_instructions
from . import arm_extra_load_store_instructions_unprivileged
from . import arm_data_processing_immediate
from .mov_immediate_a2 import MovImmediateA2
from .movt_a1 import MovtA1
from . import arm_msr_immediate_and_hints


def decode_instruction(instr):
    if not instr[6] and not (instr.bin[7:9] + instr.bin[11:12]) == "100" and not instr[27]:
        # Data-processing (register)
        return arm_data_processing_register.decode_instruction(instr)
    elif not instr[6] and not (instr.bin[7:9] + instr.bin[11:12]) == "100" and not instr[24] and instr[27]:
        # Data-processing (register-shifted register)
        return arm_data_processing_register_shifted_register.decode_instruction(instr)
    elif not instr[6] and (instr.bin[7:9] + instr.bin[11:12]) == "100" and not instr[24]:
        # Miscellaneous instructions
        return arm_miscellaneous_instructions.decode_instruction(instr)
    elif not instr[6] and (instr.bin[7:9] + instr.bin[11:12]) == "100" and instr[24] and not instr[27]:
        # Halfword multiply and multiply accumulate
        return arm_halfword_multiply_and_multiply_accumulate.decode_instruction(instr)
    elif not instr[6] and not instr[7] and instr.bin[24:28] == "1001":
        # Multiply and multiply accumulate
        return arm_multiply_and_multiply_accumulate.decode_instruction(instr)
    elif not instr[6] and instr[7] and instr.bin[24:28] == "1001":
        # Synchronization primitives
        return arm_synchronization_primitives.decode_instruction(instr)
    elif not instr[6] and ((instr[7] and not instr[10] and instr.bin[24:28] == "1011") or (
                        instr[7] and not instr[10] and instr.bin[24:26] == "11" and instr[27]) or (
                            not instr[7] and instr[10] and not instr[11] and instr.bin[24:26] == "11" and instr[27])):
        # Extra load/store instructions
        return arm_extra_load_store_instructions.decode_instruction(instr)
    elif not instr[6] and ((not instr[7] and instr[10] and instr[24:28] == "0b1011") or (
                        not instr[7] and instr[10:12] == "0b11" and instr[24:26] == "0b11" and instr[27])):
        # Extra load/store instructions, unprivileged
        return arm_extra_load_store_instructions_unprivileged.decode_instruction(instr)
    elif instr[6] and not (instr.bin[7:9] + instr.bin[11:12] == "100"):
        # Data-processing immediate
        return arm_data_processing_immediate.decode_instruction(instr)
    elif instr[6] and instr[7:12] == "0b10000":
        # 16-bit immediate load
        return MovImmediateA2
    elif instr[6] and instr[7:12] == "0b10100":
        # High halfword 16-bit immediate load
        return MovtA1
    elif instr[6] and (instr[7:9] + instr[10:12]) == "0b1010":
        # MSR (immediate), and hints
        return arm_msr_immediate_and_hints.decode_instruction(instr)
