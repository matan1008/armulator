from strb_immediate_thumb_t3 import StrbImmediateThumbT3
from strb_immediate_thumb_t2 import StrbImmediateThumbT2
from strb_register_t2 import StrbRegisterT2
from strbt_t1 import StrbtT1
from strh_immediate_thumb_t3 import StrhImmediateThumbT3
from strh_immediate_thumb_t2 import StrhImmediateThumbT2
from strh_register_t2 import StrhRegisterT2
from strht_t1 import StrhtT1
from push_t3 import PushT3
from str_immediate_thumb_t4 import StrImmediateThumbT4
from str_immediate_thumb_t3 import StrImmediateThumbT3
from str_register_t2 import StrRegisterT2
from strt_t1 import StrtT1


def decode_instruction(instr):
    if instr[8:11] == "0b000" and (instr[20:24] == "0b1100" or (instr[20] and instr[23])):
        # Store Register Byte
        return StrbImmediateThumbT3
    elif instr[8:11] == "0b100":
        # Store Register Byte
        return StrbImmediateThumbT2
    elif instr[8:11] == "0b000" and instr[20:26] == "0b000000":
        # Store Register Byte
        return StrbRegisterT2
    elif instr[8:11] == "0b000" and instr[20:24] == "0b1110":
        # Store Register Byte Unprivileged
        return StrbtT1
    elif instr[8:11] == "0b001" and (instr[20:24] == "0b1100" or (instr[20] and instr[23])):
        # Store Register Halfword
        return StrhImmediateThumbT3
    elif instr[8:11] == "0b101":
        # Store Register Halfword
        return StrhImmediateThumbT2
    elif instr[8:11] == "0b001" and instr[20:26] == "0b000000":
        # Store Register Halfword
        return StrhRegisterT2
    elif instr[8:11] == "0b001" and instr[20:24] == "0b1110":
        # Store Register Halfword Unprivileged
        return StrhtT1
    elif instr[8:11] == "0b010" and (instr[20:24] == "0b1100" or (instr[20] and instr[23])):
        # Store Register
        if instr[12:16] == "0b1101" and instr[21:24] == "0b101" and instr[24:32] == "0b00000100":
            return PushT3
        else:
            return StrImmediateThumbT4
    elif instr[8:11] == "0b110":
        # Store Register
        return StrImmediateThumbT3
    elif instr[8:11] == "0b010" and instr[20:26] == "0b000000":
        # Store Register
        return StrRegisterT2
    elif instr[8:11] == "0b010" and instr[20:24] == "0b1110":
        # Store Register Unprivileged
        return StrtT1
