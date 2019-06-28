from __future__ import absolute_import
from .ldr_register_thumb_t2 import LdrRegisterThumbT2
from .pop_thumb_t3 import PopThumbT3
from .ldr_immediate_thumb_t4 import LdrImmediateThumbT4
from .ldr_immediate_thumb_t3 import LdrImmediateThumbT3
from .ldrt_t1 import LdrtT1
from .ldr_literal_t2 import LdrLiteralT2


def decode_instruction(instr):
    if instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111":
        # Load Register
        return LdrRegisterThumbT2
    elif instr[7:9] == "0b00" and instr[12:16] != "0b1111" and (
                (instr[20] and instr[23]) or (instr[20:24] == "0b1100")):
        # Load Register
        if instr[12:16] == "0b1101" and not instr[21] and instr[22] and instr[23] and instr[24:32] == "0b00000100":
            return PopThumbT3
        else:
            return LdrImmediateThumbT4
    elif instr[7:9] == "0b01" and instr[12:16] != "0b1111":
        # Load Register
        return LdrImmediateThumbT3
    elif instr[7:9] == "0b00" and instr[12:16] != "0b1111" and instr[20:24] == "0b1110":
        # Load Register Unprivileged
        return LdrtT1
    elif not instr[7] and instr[12:16] == "0b1111":
        # Load Register
        return LdrLiteralT2
