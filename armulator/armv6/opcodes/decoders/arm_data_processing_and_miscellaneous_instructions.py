from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.concrete.mov_immediate_a2 import MovImmediateA2
from armulator.armv6.opcodes.concrete.movt_a1 import MovtA1
from armulator.armv6.opcodes.decoders import arm_data_processing_immediate
from armulator.armv6.opcodes.decoders import arm_data_processing_register
from armulator.armv6.opcodes.decoders import arm_data_processing_register_shifted_register
from armulator.armv6.opcodes.decoders import arm_extra_load_store_instructions
from armulator.armv6.opcodes.decoders import arm_extra_load_store_instructions_unprivileged
from armulator.armv6.opcodes.decoders import arm_halfword_multiply_and_multiply_accumulate
from armulator.armv6.opcodes.decoders import arm_miscellaneous_instructions
from armulator.armv6.opcodes.decoders import arm_msr_immediate_and_hints
from armulator.armv6.opcodes.decoders import arm_multiply_and_multiply_accumulate
from armulator.armv6.opcodes.decoders import arm_synchronization_primitives


def decode_instruction(instr):
    op = bit_at(instr, 25)
    instr_24 = bit_at(instr, 24)
    instr_21 = bit_at(instr, 21)
    instr_24_23_20 = chain(substring(instr, 24, 23), bit_at(instr, 20), 1)
    if not op and not instr_24_23_20 == 0b100 and not bit_at(instr, 4):
        # Data-processing (register)
        return arm_data_processing_register.decode_instruction(instr)
    elif not op and not instr_24_23_20 == 0b100 and not bit_at(instr, 7) and bit_at(instr, 4):
        # Data-processing (register-shifted register)
        return arm_data_processing_register_shifted_register.decode_instruction(instr)
    elif not op and instr_24_23_20 == 0b100 and not bit_at(instr, 7):
        # Miscellaneous instructions
        return arm_miscellaneous_instructions.decode_instruction(instr)
    elif not op and instr_24_23_20 == 0b100 and bit_at(instr, 7) and not bit_at(instr, 4):
        # Halfword multiply and multiply accumulate
        return arm_halfword_multiply_and_multiply_accumulate.decode_instruction(instr)
    elif not op and not instr_24 and substring(instr, 7, 4) == 0b1001:
        # Multiply and multiply accumulate
        return arm_multiply_and_multiply_accumulate.decode_instruction(instr)
    elif not op and instr_24 and substring(instr, 7, 4) == 0b1001:
        # Synchronization primitives
        return arm_synchronization_primitives.decode_instruction(instr)
    elif not op and (
            (not (not instr_24 and instr_21) and (
                    substring(instr, 7, 4) == 0b1011 or
                    (substring(instr, 7, 6) == 0b11 and bit_at(instr, 4)))) or
            (not instr_24 and instr_21 and substring(instr, 7, 6) == 0b11 and bit_at(instr, 4))):
        # Extra load/store instructions
        return arm_extra_load_store_instructions.decode_instruction(instr)
    elif not op and (
            (not instr_24 and instr_21 and substring(instr, 7, 4) == 0b1011) or
            (not instr_24 and substring(instr, 21, 20) == 0b11 and
             substring(instr, 7, 6) == 0b11 and bit_at(instr, 4))):
        # Extra load/store instructions, unprivileged
        return arm_extra_load_store_instructions_unprivileged.decode_instruction(instr)
    elif op and not instr_24_23_20 == 0b100:
        # Data-processing immediate
        return arm_data_processing_immediate.decode_instruction(instr)
    elif op and substring(instr, 24, 20) == 0b10000:
        # 16-bit immediate load
        return MovImmediateA2
    elif op and substring(instr, 24, 20) == 0b10100:
        # High halfword 16-bit immediate load
        return MovtA1
    elif op and chain(substring(instr, 24, 23), substring(instr, 21, 20), 2) == 0b1010:
        # MSR (immediate), and hints
        return arm_msr_immediate_and_hints.decode_instruction(instr)
