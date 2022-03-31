from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.push_t3 import PushT3
from armulator.armv6.opcodes.concrete.str_immediate_thumb_t3 import StrImmediateThumbT3
from armulator.armv6.opcodes.concrete.str_immediate_thumb_t4 import StrImmediateThumbT4
from armulator.armv6.opcodes.concrete.str_register_t2 import StrRegisterT2
from armulator.armv6.opcodes.concrete.strb_immediate_thumb_t2 import StrbImmediateThumbT2
from armulator.armv6.opcodes.concrete.strb_immediate_thumb_t3 import StrbImmediateThumbT3
from armulator.armv6.opcodes.concrete.strb_register_t2 import StrbRegisterT2
from armulator.armv6.opcodes.concrete.strbt_t1 import StrbtT1
from armulator.armv6.opcodes.concrete.strh_immediate_thumb_t2 import StrhImmediateThumbT2
from armulator.armv6.opcodes.concrete.strh_immediate_thumb_t3 import StrhImmediateThumbT3
from armulator.armv6.opcodes.concrete.strh_register_t2 import StrhRegisterT2
from armulator.armv6.opcodes.concrete.strht_t1 import StrhtT1
from armulator.armv6.opcodes.concrete.strt_t1 import StrtT1


def decode_instruction(instr):
    instr_op1 = substring(instr, 23, 21)
    instr_op2 = substring(instr, 11, 6)
    instr_11_8 = substring(instr, 11, 8)
    if instr_op1 == 0b000 and (instr_11_8 == 0b1100 or (bit_at(instr, 11) and bit_at(instr, 8))):
        # Store Register Byte
        return StrbImmediateThumbT3
    elif instr_op1 == 0b100:
        # Store Register Byte
        return StrbImmediateThumbT2
    elif instr_op1 == 0b000 and instr_op2 == 0b000000:
        # Store Register Byte
        return StrbRegisterT2
    elif instr_op1 == 0b000 and instr_11_8 == 0b1110:
        # Store Register Byte Unprivileged
        return StrbtT1
    elif instr_op1 == 0b001 and (instr_11_8 == 0b1100 or (bit_at(instr, 11) and bit_at(instr, 8))):
        # Store Register Halfword
        return StrhImmediateThumbT3
    elif instr_op1 == 0b101:
        # Store Register Halfword
        return StrhImmediateThumbT2
    elif instr_op1 == 0b001 and instr_op2 == 0b000000:
        # Store Register Halfword
        return StrhRegisterT2
    elif instr_op1 == 0b001 and instr_11_8 == 0b1110:
        # Store Register Halfword Unprivileged
        return StrhtT1
    elif instr_op1 == 0b010 and (instr_11_8 == 0b1100 or (bit_at(instr, 11) and bit_at(instr, 8))):
        # Store Register
        if substring(instr, 19, 16) == 0b1101 and substring(instr, 10, 0) == 0b10100000100:
            return PushT3
        else:
            return StrImmediateThumbT4
    elif instr_op1 == 0b110:
        # Store Register
        return StrImmediateThumbT3
    elif instr_op1 == 0b010 and instr_op2 == 0b000000:
        # Store Register
        return StrRegisterT2
    elif instr_op1 == 0b010 and instr_11_8 == 0b1110:
        # Store Register Unprivileged
        return StrtT1
