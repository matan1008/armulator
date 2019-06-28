from __future__ import absolute_import
from . import thumb_instruction_set_encoding_16_bit
from . import thumb_instruction_set_encoding_32_bit


def decode_instruction(instr):
    if instr.len == 16:
        # 16-bit Thumb instruction encoding
        return thumb_instruction_set_encoding_16_bit.decode_instruction(instr)
    elif instr.len == 32:
        # 32-bit Thumb instruction encoding
        return thumb_instruction_set_encoding_32_bit.decode_instruction(instr)
