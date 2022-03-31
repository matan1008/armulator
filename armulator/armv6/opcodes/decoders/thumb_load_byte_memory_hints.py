from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldrb_immediate_thumb_t2 import LdrbImmediateThumbT2
from armulator.armv6.opcodes.concrete.ldrb_immediate_thumb_t3 import LdrbImmediateThumbT3
from armulator.armv6.opcodes.concrete.ldrb_literal_t1 import LdrbLiteralT1
from armulator.armv6.opcodes.concrete.ldrb_register_t2 import LdrbRegisterT2
from armulator.armv6.opcodes.concrete.ldrbt_t1 import LdrbtT1
from armulator.armv6.opcodes.concrete.ldrsb_immediate_t1 import LdrsbImmediateT1
from armulator.armv6.opcodes.concrete.ldrsb_immediate_t2 import LdrsbImmediateT2
from armulator.armv6.opcodes.concrete.ldrsb_literal_t1 import LdrsbLiteralT1
from armulator.armv6.opcodes.concrete.ldrsb_register_t2 import LdrsbRegisterT2
from armulator.armv6.opcodes.concrete.ldrsbt_t1 import LdrsbtT1
from armulator.armv6.opcodes.concrete.pld_immediate_t1 import PldImmediateT1
from armulator.armv6.opcodes.concrete.pld_immediate_t2 import PldImmediateT2
from armulator.armv6.opcodes.concrete.pld_literal_t1 import PldLiteralT1
from armulator.armv6.opcodes.concrete.pld_register_t1 import PldRegisterT1


def decode_instruction(instr):
    op1 = substring(instr, 24, 23)
    op2 = substring(instr, 11, 6)
    rn = substring(instr, 19, 16)
    rt = substring(instr, 15, 12)
    if op1 == 0b00 and op2 == 0b000000 and rn != 0b1111 and rt != 0b1111:
        # Load Register Byte
        return LdrbRegisterT2
    elif op1 == 0b00 and op2 == 0b000000 and rn != 0b1111 and rt == 0b1111:
        # Preload Data
        return PldRegisterT1
    elif not bit_at(instr, 24) and op2 == 0b000000 and rn == 0b1111 and rt != 0b1111:
        # Load Register Byte
        return LdrbLiteralT1
    elif not bit_at(instr, 24) and op2 == 0b000000 and rn == 0b1111 and rt == 0b1111:
        # Preload Data
        return PldLiteralT1
    elif op1 == 0b00 and rn != 0b1111 and (
            (bit_at(instr, 11) and bit_at(instr, 8)) or (
            substring(instr, 11, 8) == 0b1100 and rn != 0b1111 and rt != 0b1111)):
        # Load Register Byte
        return LdrbImmediateThumbT3
    elif op1 == 0b00 and substring(instr, 11, 8) == 0b1100 and rn != 0b1111 and rt == 0b1111:
        # Preload Data
        return PldImmediateT2
    elif op1 == 0b00 and substring(instr, 11, 8) == 0b1110 and rn != 0b1111:
        # Load Register Byte Unprivileged
        return LdrbtT1
    elif op1 == 0b01 and rn != 0b1111 and rt != 0b1111:
        # Load Register Byte
        return LdrbImmediateThumbT2
    elif op1 == 0b01 and rn != 0b1111 and rt == 0b1111:
        # Preload Data
        return PldImmediateT1
    elif op1 == 0b10 and op2 == 0b000000 and rn != 0b1111 and rt != 0b1111:
        # Load Register Signed Byte
        return LdrsbRegisterT2
    elif op1 == 0b00 and op2 == 0b000000 and rn != 0b1111 and rt == 0b1111:
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif bit_at(instr, 24) and op2 == 0b000000 and rn == 0b1111 and rt != 0b1111:
        # Load Register Signed Byte
        return LdrsbLiteralT1
    elif bit_at(instr, 24) and op2 == 0b000000 and rn == 0b1111 and rt == 0b1111:
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif op1 == 0b10 and rn != 0b1111 and (
            (bit_at(instr, 11) and bit_at(instr, 8)) or (substring(instr, 11, 8) == 0b1100 and rn != 0b1111)):
        # Load Register Signed Byte
        return LdrsbImmediateT2
    elif op1 == 0b10 and substring(instr, 11, 8) == 0b1100 and rn != 0b1111 and rt == 0b1111:
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
    elif op1 == 0b10 and substring(instr, 11, 8) == 0b1110 and rn != 0b1111:
        # Load Register Signed Byte Unprivileged
        return LdrsbtT1
    elif op1 == 0b11 and rn != 0b1111 and rt != 0b1111:
        # Load Register Signed Byte
        return LdrsbImmediateT1
    elif op1 == 0b11 and rn != 0b1111 and rt == 0b1111:
        # Preload Instruction
        # armv7, will not be implemented
        raise NotImplementedError()
