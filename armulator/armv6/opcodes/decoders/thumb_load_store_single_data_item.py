from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t1 import LdrImmediateThumbT1
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t2 import LdrImmediateThumbT2
from armulator.armv6.opcodes.concrete.ldr_register_thumb_t1 import LdrRegisterThumbT1
from armulator.armv6.opcodes.concrete.ldrb_immediate_thumb_t1 import LdrbImmediateThumbT1
from armulator.armv6.opcodes.concrete.ldrb_register_t1 import LdrbRegisterT1
from armulator.armv6.opcodes.concrete.ldrh_immediate_thumb_t1 import LdrhImmediateThumbT1
from armulator.armv6.opcodes.concrete.ldrh_register_t1 import LdrhRegisterT1
from armulator.armv6.opcodes.concrete.ldrsb_register_t1 import LdrsbRegisterT1
from armulator.armv6.opcodes.concrete.ldrsh_register_t1 import LdrshRegisterT1
from armulator.armv6.opcodes.concrete.str_immediate_thumb_t1 import StrImmediateThumbT1
from armulator.armv6.opcodes.concrete.str_immediate_thumb_t2 import StrImmediateThumbT2
from armulator.armv6.opcodes.concrete.str_register_t1 import StrRegisterT1
from armulator.armv6.opcodes.concrete.strb_immediate_thumb_t1 import StrbImmediateThumbT1
from armulator.armv6.opcodes.concrete.strb_register_t1 import StrbRegisterT1
from armulator.armv6.opcodes.concrete.strh_immediate_thumb_t1 import StrhImmediateThumbT1
from armulator.armv6.opcodes.concrete.strh_register_t1 import StrhRegisterT1


def decode_instruction(instr):
    if substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b000:
        # Store Register
        return StrRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b001:
        # Store Register Halfword
        return StrhRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b010:
        # Store Register Byte
        return StrbRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b011:
        # Load Register Signed Byte
        return LdrsbRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b100:
        # Load Register
        return LdrRegisterThumbT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b101:
        # Load Register Halfword
        return LdrhRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b110:
        # Load Register Byte
        return LdrbRegisterT1
    elif substring(instr, 15, 12) == 0b0101 and substring(instr, 11, 9) == 0b111:
        # Load Register Signed Halfword
        return LdrshRegisterT1
    elif substring(instr, 15, 12) == 0b0110 and not bit_at(instr, 11):
        # Store Register
        return StrImmediateThumbT1
    elif substring(instr, 15, 12) == 0b0110 and bit_at(instr, 11):
        # Load Register
        return LdrImmediateThumbT1
    elif substring(instr, 15, 12) == 0b0111 and not bit_at(instr, 11):
        # Store Register Byte
        return StrbImmediateThumbT1
    elif substring(instr, 15, 12) == 0b0111 and bit_at(instr, 11):
        # Load Register Byte
        return LdrbImmediateThumbT1
    elif substring(instr, 15, 12) == 0b1000 and not bit_at(instr, 11):
        # Store Register Halfword
        return StrhImmediateThumbT1
    elif substring(instr, 15, 12) == 0b1000 and bit_at(instr, 11):
        # Load Register Halfword
        return LdrhImmediateThumbT1
    elif substring(instr, 15, 12) == 0b1001 and not bit_at(instr, 11):
        # Store Register SP relative
        return StrImmediateThumbT2
    elif substring(instr, 15, 12) == 0b1001 and bit_at(instr, 11):
        # Load Register SP relative
        return LdrImmediateThumbT2
