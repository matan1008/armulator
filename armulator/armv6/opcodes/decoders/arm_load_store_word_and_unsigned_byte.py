from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.concrete.ldr_immediate_arm_a1 import LdrImmediateArmA1
from armulator.armv6.opcodes.concrete.ldr_literal_a1 import LdrLiteralA1
from armulator.armv6.opcodes.concrete.ldr_register_arm_a1 import LdrRegisterArmA1
from armulator.armv6.opcodes.concrete.ldrb_immediate_arm_a1 import LdrbImmediateArmA1
from armulator.armv6.opcodes.concrete.ldrb_literal_a1 import LdrbLiteralA1
from armulator.armv6.opcodes.concrete.ldrb_register_a1 import LdrbRegisterA1
from armulator.armv6.opcodes.concrete.ldrbt_a1 import LdrbtA1
from armulator.armv6.opcodes.concrete.ldrbt_a2 import LdrbtA2
from armulator.armv6.opcodes.concrete.ldrt_a1 import LdrtA1
from armulator.armv6.opcodes.concrete.ldrt_a2 import LdrtA2
from armulator.armv6.opcodes.concrete.pop_arm_a2 import PopArmA2
from armulator.armv6.opcodes.concrete.push_a2 import PushA2
from armulator.armv6.opcodes.concrete.str_immediate_arm_a1 import StrImmediateArmA1
from armulator.armv6.opcodes.concrete.str_register_a1 import StrRegisterA1
from armulator.armv6.opcodes.concrete.strb_immediate_arm_a1 import StrbImmediateArmA1
from armulator.armv6.opcodes.concrete.strb_register_a1 import StrbRegisterA1
from armulator.armv6.opcodes.concrete.strbt_a1 import StrbtA1
from armulator.armv6.opcodes.concrete.strbt_a2 import StrbtA2
from armulator.armv6.opcodes.concrete.strt_a1 import StrtA1
from armulator.armv6.opcodes.concrete.strt_a2 import StrtA2


def decode_instruction(instr):
    a = bit_at(instr, 25)
    b = bit_at(instr, 4)
    op1_0 = bit_at(instr, 20)
    op1_2 = bit_at(instr, 22)
    op1_2_0 = substring(instr, 22, 20)
    op1_4 = bit_at(instr, 24)
    rn = substring(instr, 19, 16)
    instr_23 = bit_at(instr, 23)
    instr_21 = bit_at(instr, 21)
    instr_11_0 = substring(instr, 11, 0)
    if not a and not op1_2 and not op1_0 and not (not op1_4 and op1_2_0 == 0b010):
        # Store Register immediate ARM
        if rn == 0b1101 and op1_4 and not instr_23 and instr_21 and instr_11_0 == 0b000000000100:
            return PushA2
        else:
            return StrImmediateArmA1
    elif a and not b and not op1_2 and not op1_0 and not (not op1_4 and op1_2_0 == 0b010):
        # Store Register register
        return StrRegisterA1
    elif not a and not op1_4 and op1_2_0 == 0b010:
        # Store Register Unprivileged
        return StrtA1
    elif a and not b and not op1_4 and op1_2_0 == 0b010:
        # Store Register Unprivileged
        return StrtA2
    elif not a and not op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b011) and rn != 0b1111:
        # Load Register (immediate) arm
        if rn == 0b1101 and not op1_4 and instr_23 and not instr_21 and instr_11_0 == 0b000000000100:
            return PopArmA2
        else:
            return LdrImmediateArmA1
    elif not a and not op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b011) and rn == 0b1111:
        # Load Register (literal)
        return LdrLiteralA1
    elif a and not b and not op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b011):
        # Load Register register arm
        return LdrRegisterArmA1
    elif not a and not op1_4 and op1_2_0 == 0b011:
        # Load Register Unprivileged
        return LdrtA1
    elif a and not b and not op1_4 and op1_2_0 == 0b011:
        # Load Register Unprivileged
        return LdrtA2
    elif not a and op1_2 and not op1_0 and not (not op1_4 and op1_2_0 == 0b110):
        # Store Register Byte (immediate) arm
        return StrbImmediateArmA1
    elif a and not b and op1_2 and not op1_0 and not (not op1_4 and op1_2_0 == 0b110):
        # Store Register Byte (register)
        return StrbRegisterA1
    elif not a and not op1_4 and op1_2_0 == 0b110:
        # Store Register Byte Unprivileged
        return StrbtA1
    elif a and not b and not op1_4 and op1_2_0 == 0b110:
        # Store Register Byte Unprivileged
        return StrbtA2
    elif not a and op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b111) and rn != 0b1111:
        # Load Register Byte (immediate) arm
        return LdrbImmediateArmA1
    elif not a and op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b111) and rn == 0b1111:
        # Load Register Byte (literal)
        return LdrbLiteralA1
    elif a and not b and op1_2 and op1_0 and not (not op1_4 and op1_2_0 == 0b111):
        # Load Register Byte (register)
        return LdrbRegisterA1
    elif not a and not op1_4 and op1_2_0 == 0b111:
        # Load Register Byte Unprivileged
        return LdrbtA1
    elif a and not b and not op1_4 and op1_2_0 == 0b111:
        # Load Register Byte Unprivileged
        return LdrbtA2
