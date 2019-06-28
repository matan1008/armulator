from __future__ import absolute_import
from .strh_register_a1 import StrhRegisterA1
from .ldrh_register_a1 import LdrhRegisterA1
from .strh_immediate_arm_a1 import StrhImmediateArmA1
from .ldrh_immediate_arm_a1 import LdrhImmediateArmA1
from .ldrh_literal_a1 import LdrhLiteralA1
from .ldrd_register_a1 import LdrdRegisterA1
from .ldrsb_register_a1 import LdrsbRegisterA1
from .ldrd_immediate_a1 import LdrdImmediateA1
from .ldrd_literal_a1 import LdrdLiteralA1
from .ldrsb_immediate_a1 import LdrsbImmediateA1
from .ldrsb_literal_a1 import LdrsbLiteralA1
from .strd_register_a1 import StrdRegisterA1
from .ldrsh_register_a1 import LdrshRegisterA1
from .strd_immediate_a1 import StrdImmediateA1
from .ldrsh_immediate_a1 import LdrshImmediateA1
from .ldrsh_literal_a1 import LdrshLiteralA1


def decode_instruction(instr):
    if instr[25:27] == "0b01" and not instr[9] and not instr[11]:
        # Store Halfword register
        return StrhRegisterA1
    elif instr[25:27] == "0b01" and not instr[9] and instr[11]:
        # Load Halfword register
        return LdrhRegisterA1
    elif instr[25:27] == "0b01" and instr[9] and not instr[11]:
        # Store Halfword immediate arm
        return StrhImmediateArmA1
    elif instr[25:27] == "0b01" and instr[9] and instr[11] and instr[12:16] != "0b1111":
        # Load Halfword immediate arm
        return LdrhImmediateArmA1
    elif instr[25:27] == "0b01" and instr[9] and instr[11] and instr[12:16] == "0b1111":
        # Load Halfword literal
        return LdrhLiteralA1
    elif instr[25:27] == "0b10" and not instr[9] and not instr[11]:
        # Load Dual register
        return LdrdRegisterA1
    elif instr[25:27] == "0b10" and not instr[9] and instr[11]:
        # Load Signed Byte register
        return LdrsbRegisterA1
    elif instr[25:27] == "0b10" and instr[9] and not instr[11] and instr[12:16] != "0b1111":
        # Load Dual immediate
        return LdrdImmediateA1
    elif instr[25:27] == "0b10" and instr[9] and not instr[11] and instr[12:16] == "0b1111":
        # Load Dual literal
        return LdrdLiteralA1
    elif instr[25:27] == "0b10" and instr[9] and instr[11] and instr[12:16] != "0b1111":
        # Load Signed Byte immediate
        return LdrsbImmediateA1
    elif instr[25:27] == "0b10" and instr[9] and instr[11] and instr[12:16] == "0b1111":
        # Load Signed Byte literal
        return LdrsbLiteralA1
    elif instr[25:27] == "0b11" and not instr[9] and not instr[11]:
        # Store Dual register
        return StrdRegisterA1
    elif instr[25:27] == "0b11" and not instr[9] and instr[11]:
        # Load Signed Halfword register
        return LdrshRegisterA1
    elif instr[25:27] == "0b11" and instr[9] and not instr[11]:
        # Store Dual immediate
        return StrdImmediateA1
    elif instr[25:27] == "0b11" and instr[9] and instr[11] and instr[12:16] != "0b1111":
        # Load Signed Halfword immediate
        return LdrshImmediateA1
    elif instr[25:27] == "0b11" and instr[9] and instr[11] and instr[12:16] == "0b1111":
        # Load Signed Halfword literal
        return LdrshLiteralA1
