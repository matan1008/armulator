from ldrb_register_t2 import LdrbRegisterT2
from pld_register_t1 import PldRegisterT1
from ldrb_literal_t1 import LdrbLiteralT1
from pld_literal_t1 import PldLiteralT1
from ldrb_immediate_thumb_t3 import LdrbImmediateThumbT3
from pld_immediate_t2 import PldImmediateT2
from ldrbt_t1 import LdrbtT1
from ldrb_immediate_thumb_t2 import LdrbImmediateThumbT2
from pld_immediate_t1 import PldImmediateT1
from ldrsb_register_t2 import LdrsbRegisterT2
from ldrsb_literal_t1 import LdrsbLiteralT1
from ldrsb_immediate_t2 import LdrsbImmediateT2
from ldrsbt_t1 import LdrsbtT1
from ldrsb_immediate_t1 import LdrsbImmediateT1


def decode_instruction(instr):
    if instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Byte
        return LdrbRegisterT2
    elif instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data
        return PldRegisterT1
    elif not instr[7] and instr[20:26] == "0b000000" and instr[12:16] == "0b1111" and instr[16:20] != "0b1111":
        # Load Register Byte
        return LdrbLiteralT1
    elif not instr[7] and instr[20:26] == "0b000000" and instr[12:16] == "0b1111" and instr[16:20] == "0b1111":
        # Preload Data
        return PldLiteralT1
    elif instr[7:9] == "0b00" and instr[12:16] != "0b1111" and (
                (instr[20] and instr[23]) or (instr[20:24] == "0b1100" and instr[12:16] != "0b1111")):
        # Load Register Byte
        return LdrbImmediateThumbT3
    elif instr[7:9] == "0b00" and instr[20:24] == "0b1100" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data
        return PldImmediateT2
    elif instr[7:9] == "0b00" and instr[20:24] == "0b1110" and instr[12:16] != "0b1111":
        # Load Register Byte Unprivileged
        return LdrbtT1
    elif instr[7:9] == "0b01" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Byte
        return LdrbImmediateThumbT2
    elif instr[7:9] == "0b01" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data
        return PldImmediateT1
    elif instr[7:9] == "0b10" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Byte
        return LdrsbRegisterT2
    elif instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr[7] and instr[20:26] == "0b000000" and instr[12:16] == "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Byte
        return LdrsbLiteralT1
    elif instr[7] and instr[20:26] == "0b000000" and instr[12:16] == "0b1111" and instr[16:20] == "0b1111":
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr[7:9] == "0b10" and instr[12:16] != "0b1111" and (
                (instr[20] and instr[23]) or (instr[20:24] == "0b1100" and instr[12:16] != "0b1111")):
        # Load Register Signed Byte
        return LdrsbImmediateT2
    elif instr[7:9] == "0b10" and instr[20:24] == "0b1100" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif instr[7:9] == "0b10" and instr[20:24] == "0b1110" and instr[12:16] != "0b1111":
        # Load Register Signed Byte Unprivileged
        return LdrsbtT1
    elif instr[7:9] == "0b11" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Byte
        return LdrsbImmediateT1
    elif instr[7:9] == "0b11" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
