from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldrh_immediate_thumb_t2 import LdrhImmediateThumbT2
from armulator.armv6.opcodes.concrete.ldrh_immediate_thumb_t3 import LdrhImmediateThumbT3
from armulator.armv6.opcodes.concrete.ldrh_literal_t1 import LdrhLiteralT1
from armulator.armv6.opcodes.concrete.ldrh_register_t2 import LdrhRegisterT2
from armulator.armv6.opcodes.concrete.ldrht_t1 import LdrhtT1
from armulator.armv6.opcodes.concrete.pld_immediate_t1 import PldImmediateT1
from armulator.armv6.opcodes.concrete.pld_immediate_t2 import PldImmediateT2
from armulator.armv6.opcodes.concrete.pld_literal_t1 import PldLiteralT1
from armulator.armv6.opcodes.concrete.pld_register_t1 import PldRegisterT1
from armulator.armv6.opcodes.concrete.ldrsh_immediate_t1 import LdrshImmediateT1
from armulator.armv6.opcodes.concrete.ldrsh_immediate_t2 import LdrshImmediateT2
from armulator.armv6.opcodes.concrete.ldrsh_literal_t1 import LdrshLiteralT1
from armulator.armv6.opcodes.concrete.ldrsh_register_t2 import LdrshRegisterT2
from armulator.armv6.opcodes.concrete.ldrsht_t1 import LdrshtT1


def decode_instruction(instr):
    op1 = substring(instr, 24, 23)
    op2 = substring(instr, 11, 6)
    rn = substring(instr, 19, 16)
    rt = substring(instr, 15, 12)
    if not bit_at(instr, 24) and rn == 0b1111 and rt != 0b1111:
        # Load Register Halfword
        return LdrhLiteralT1
    elif not bit_at(instr, 24) and rn == 0b1111 and rt == 0b1111:
        # Preload Data
        return PldLiteralT1
    elif op1 == 0b00 and rn != 0b1111 and (
            (bit_at(instr, 11) and bit_at(instr, 8)) or (substring(instr, 11, 8) == 0b1100 and rt != 0b1111)):
        # Load Register Halfword
        return LdrhImmediateThumbT3
    elif op1 == 0b01 and rn != 0b1111 and rt != 0b1111:
        # Load Register Halfword
        return LdrhImmediateThumbT2
    elif op1 == 0b00 and op2 == 0b000000 and rn != 0b1111 and rt != 0b1111:
        # Load Register Halfword
        return LdrhRegisterT2
    elif op1 == 0b00 and substring(instr, 11, 8) == 0b1110 and rn != 0b1111:
        # Load Register Halfword Unprivileged
        return LdrhtT1
    elif op1 == 0b00 and op2 == 0b000000 and rn != 0b1111 and rt == 0b1111:
        # Preload Data with intent to Write
        return PldRegisterT1
    elif op1 == 0b00 and substring(instr, 11, 8) == 0b1100 and rn != 0b1111 and rt == 0b1111:
        # Preload Data with intent to Write
        return PldImmediateT2
    elif op1 == 0b01 and rn != 0b1111 and rt == 0b1111:
        # Preload Data with intent to Write
        return PldImmediateT1
    elif op1 == 0b10 and rn != 0b1111 and (
            (bit_at(instr, 11) and bit_at(instr, 8)) or (substring(instr, 11, 8) == 0b1100 and rt != 0b1111)):
        # Load Register Signed Halfword
        return LdrshImmediateT2
    elif op1 == 0b11 and rn != 0b1111 and rt != 0b1111:
        # Load Register Signed Halfword
        return LdrshImmediateT1
    elif bit_at(instr, 24) and rn == 0b1111 and rt != 0b1111:
        # Load Register Signed Halfword
        return LdrshLiteralT1
    elif op1 == 0b10 and op2 == 0b000000 and rn != 0b1111 and rt != 0b1111:
        # Load Register Signed Halfword
        return LdrshRegisterT2
    elif op1 == 0b10 and substring(instr, 11, 8) == 0b1110 and rn != 0b1111:
        # Load Register Signed Halfword Unprivileged
        return LdrshtT1
