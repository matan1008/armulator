from ldrh_literal_t1 import LdrhLiteralT1
from pld_literal_t1 import PldLiteralT1
from ldrh_immediate_thumb_t3 import LdrhImmediateThumbT3
from ldrh_immediate_thumb_t2 import LdrhImmediateThumbT2
from ldrh_register_t2 import LdrhRegisterT2
from ldrht_t1 import LdrhtT1
from pld_register_t1 import PldRegisterT1
from pld_immediate_t2 import PldImmediateT2
from pld_immediate_t1 import PldImmediateT1
from ldrsh_immediate_t2 import LdrshImmediateT2
from ldrsh_immediate_t1 import LdrshImmediateT1
from ldrsh_literal_t1 import LdrshLiteralT1
from ldrsh_register_t2 import LdrshRegisterT2
from ldrsht_t1 import LdrshtT1


def decode_instruction(instr):
    if not instr[7] and instr[12:16] == "0b1111" and instr[16:20] != "0b1111":
        # Load Register Halfword
        return LdrhLiteralT1
    elif not instr[7] and instr[12:16] == "0b1111" and instr[16:20] == "0b1111":
        # Preload Data
        return PldLiteralT1
    elif instr[7:9] == "0b00" and instr[12:16] != "0b1111" and (
                (instr[20] and instr[23]) or (instr[20:24] == "0b1100" and instr[16:20] != "0b1111")):
        # Load Register Halfword
        return LdrhImmediateThumbT3
    elif instr[7:9] == "0b01" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Halfword
        return LdrhImmediateThumbT2
    elif instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Halfword
        return LdrhRegisterT2
    elif instr[7:9] == "0b00" and instr[20:24] == "0b1110" and instr[12:16] != "0b1111":
        # Load Register Halfword Unprivileged
        return LdrhtT1
    elif instr[7:9] == "0b00" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data with intent to Write
        return PldRegisterT1
    elif instr[7:9] == "0b00" and instr[20:24] == "0b1100" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data with intent to Write
        return PldImmediateT2
    elif instr[7:9] == "0b01" and instr[12:16] != "0b1111" and instr[16:20] == "0b1111":
        # Preload Data with intent to Write
        return PldImmediateT1
    elif instr[7:9] == "0b10" and instr[12:16] != "0b1111" and (
                (instr[20] and instr[23]) or (instr[20:24] == "0b1100" and instr[16:20] != "0b1111")):
        # Load Register Signed Halfword
        return LdrshImmediateT2
    elif instr[7:9] == "0b11" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Halfword
        return LdrshImmediateT1
    elif instr[7] and instr[12:16] == "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Halfword
        return LdrshLiteralT1
    elif instr[7:9] == "0b10" and instr[20:26] == "0b000000" and instr[12:16] != "0b1111" and instr[16:20] != "0b1111":
        # Load Register Signed Halfword
        return LdrshRegisterT2
    elif instr[7:9] == "0b10" and instr[20:24] == "0b1110" and instr[12:16] != "0b1111":
        # Load Register Signed Halfword Unprivileged
        return LdrshtT1
