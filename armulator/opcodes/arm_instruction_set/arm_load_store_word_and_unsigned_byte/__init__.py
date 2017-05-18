from push_a2 import PushA2
from str_immediate_arm_a1 import StrImmediateArmA1
from str_register_a1 import StrRegisterA1
from strt_a1 import StrtA1
from strt_a2 import StrtA2
from pop_arm_a2 import PopArmA2
from ldr_immediate_arm_a1 import LdrImmediateArmA1
from ldr_literal_a1 import LdrLiteralA1
from ldr_register_arm_a1 import LdrRegisterArmA1
from ldrt_a1 import LdrtA1
from ldrt_a2 import LdrtA2
from strb_immediate_arm_a1 import StrbImmediateArmA1
from strb_register_a1 import StrbRegisterA1
from strbt_a1 import StrbtA1
from strbt_a2 import StrbtA2
from ldrb_immediate_arm_a1 import LdrbImmediateArmA1
from ldrb_literal_a1 import LdrbLiteralA1
from ldrb_register_a1 import LdrbRegisterA1
from ldrbt_a1 import LdrbtA1
from ldrbt_a2 import LdrbtA2


def decode_instruction(instr):
    if not instr[6] and not instr[9] and not instr[11] and not (not instr[7] and instr[10]):
        # Store Register immediate ARM
        if instr[12:16] == "0b1101" and instr[7] and not instr[8] and instr[10] and instr[20:32] == "0b000000000100":
            return PushA2
        else:
            return StrImmediateArmA1
    elif instr[6] and not instr[27] and not instr[9] and not instr[11] and not (
                not instr[7] and instr[10]):
        # Store Register register
        return StrRegisterA1
    elif not instr[6] and not instr[7] and instr[9:12] == "0b010":
        # Store Register Unprivileged
        return StrtA1
    elif instr[6] and not instr[27] and not instr[7] and instr[9:12] == "0b010":
        # Store Register Unprivileged
        return StrtA2
    elif not instr[6] and not instr[9] and instr[11] and not (
                not instr[7] and instr[10]) and instr[12:16] != "0b1111":
        # Load Register (immediate) arm
        if instr[12:16] == "0b1101" and not instr[7] and instr[8] and not instr[10] and instr[
                                                                                        20:32] == "0b000000000100":
            return PopArmA2
        else:
            return LdrImmediateArmA1
    elif not instr[6] and not instr[9] and instr[11] and not (
                not instr[7] and instr[10]) and instr[12:16] == "0b1111":
        # Load Register (literal)
        return LdrLiteralA1
    elif instr[6] and not instr[27] and not instr[9] and instr[11] and not (
                not instr[7] and instr[10]):
        # Load Register register arm
        return LdrRegisterArmA1
    elif not instr[6] and not instr[7] and instr[9:12] == "0b011":
        # Load Register Unprivileged
        return LdrtA1
    elif instr[6] and not instr[27] and not instr[7] and instr[9:12] == "0b011":
        # Load Register Unprivileged
        return LdrtA2
    elif not instr[6] and instr[9] and not instr[11] and not (not instr[7] and instr[10]):
        # Store Register Byte (immediate) arm
        return StrbImmediateArmA1
    elif instr[6] and not instr[27] and instr[9] and not instr[11] and not (
                not instr[7] and instr[10]):
        # Store Register Byte (register)
        return StrbRegisterA1
    elif not instr[6] and not instr[7] and instr[9:12] == "0b110":
        # Store Register Byte Unprivileged
        return StrbtA1
    elif instr[6] and not instr[27] and not instr[7] and instr[9:12] == "0b110":
        # Store Register Byte Unprivileged
        return StrbtA2
    elif not instr[6] and instr[9] and instr[11] and not (
                not instr[7] and instr[10]) and instr[12:16] != "0b1111":
        # Load Register Byte (immediate) arm
        return LdrbImmediateArmA1
    elif not instr[6] and instr[9] and instr[11] and not (
                not instr[7] and instr[10]) and instr[12:16] == "0b1111":
        # Load Register Byte (literal)
        return LdrbLiteralA1
    elif instr[6] and not instr[27] and instr[9] and instr[11] and not (
                not instr[7] and instr[10]):
        # Load Register Byte (register)
        return LdrbRegisterA1
    elif not instr[6] and not instr[7] and instr[9:12] == "0b111":
        # Load Register Byte Unprivileged
        return LdrbtA1
    elif instr[6] and not instr[27] and not instr[7] and instr[9:12] == "0b111":
        # Load Register Byte Unprivileged
        return LdrbtA2
