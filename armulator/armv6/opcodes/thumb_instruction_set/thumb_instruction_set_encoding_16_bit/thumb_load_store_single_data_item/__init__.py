from str_register_t1 import StrRegisterT1
from strh_register_t1 import StrhRegisterT1
from strb_register_t1 import StrbRegisterT1
from ldrsb_register_t1 import LdrsbRegisterT1
from ldr_register_thumb_t1 import LdrRegisterThumbT1
from ldrh_register_t1 import LdrhRegisterT1
from ldrb_register_t1 import LdrbRegisterT1
from ldrsh_register_t1 import LdrshRegisterT1
from str_immediate_thumb_t1 import StrImmediateThumbT1
from ldr_immediate_thumb_t1 import LdrImmediateThumbT1
from strb_immediate_thumb_t1 import StrbImmediateThumbT1
from ldrb_immediate_thumb_t1 import LdrbImmediateThumbT1
from strh_immediate_thumb_t1 import StrhImmediateThumbT1
from ldrh_immediate_thumb_t1 import LdrhImmediateThumbT1
from str_immediate_thumb_t2 import StrImmediateThumbT2
from ldr_immediate_thumb_t2 import LdrImmediateThumbT2


def decode_instruction(instr):
    if instr[0:4] == "0b0101" and instr[4:7] == "0b000":
        # Store Register
        return StrRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b001":
        # Store Register Halfword
        return StrhRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b010":
        # Store Register Byte
        return StrbRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b011":
        # Load Register Signed Byte
        return LdrsbRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b100":
        # Load Register
        return LdrRegisterThumbT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b101":
        # Load Register Halfword
        return LdrhRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b110":
        # Load Register Byte
        return LdrbRegisterT1
    elif instr[0:4] == "0b0101" and instr[4:7] == "0b111":
        # Load Register Signed Halfword
        return LdrshRegisterT1
    elif instr[0:4] == "0b0110" and not instr[4]:
        # Store Register
        return StrImmediateThumbT1
    elif instr[0:4] == "0b0110" and instr[4]:
        # Load Register
        return LdrImmediateThumbT1
    elif instr[0:4] == "0b0111" and not instr[4]:
        # Store Register Byte
        return StrbImmediateThumbT1
    elif instr[0:4] == "0b0111" and instr[4]:
        # Load Register Byte
        return LdrbImmediateThumbT1
    elif instr[0:4] == "0b1000" and not instr[4]:
        # Store Register Halfword
        return StrhImmediateThumbT1
    elif instr[0:4] == "0b1000" and instr[4]:
        # Load Register Halfword
        return LdrhImmediateThumbT1
    elif instr[0:4] == "0b1001" and not instr[4]:
        # Store Register SP relative
        return StrImmediateThumbT2
    elif instr[0:4] == "0b1001" and instr[4]:
        # Load Register SP relative
        return LdrImmediateThumbT2
