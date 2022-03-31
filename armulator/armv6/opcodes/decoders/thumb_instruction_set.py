from armulator.armv6.opcodes.decoders import thumb_instruction_set_encoding_16_bit
from armulator.armv6.opcodes.decoders import thumb_instruction_set_encoding_32_bit


def decode_instruction(instr, processor):
    if processor.this_instr_length() == 16:
        # 16-bit Thumb instruction encoding
        return thumb_instruction_set_encoding_16_bit.decode_instruction(instr)
    elif processor.this_instr_length() == 32:
        # 32-bit Thumb instruction encoding
        return thumb_instruction_set_encoding_32_bit.decode_instruction(instr)
