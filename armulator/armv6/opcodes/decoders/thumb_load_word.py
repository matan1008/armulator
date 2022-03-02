from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t3 import LdrImmediateThumbT3
from armulator.armv6.opcodes.concrete.ldr_immediate_thumb_t4 import LdrImmediateThumbT4
from armulator.armv6.opcodes.concrete.ldr_literal_t2 import LdrLiteralT2
from armulator.armv6.opcodes.concrete.ldr_register_thumb_t2 import LdrRegisterThumbT2
from armulator.armv6.opcodes.concrete.ldrt_t1 import LdrtT1
from armulator.armv6.opcodes.concrete.pop_thumb_t3 import PopThumbT3


def decode_instruction(instr):
    op1 = substring(instr, 24, 23)
    op2 = substring(instr, 11, 6)
    rn = substring(instr, 19, 16)
    if op1 == 0b00 and op2 == 0b000000 and rn != 0b1111:
        # Load Register
        return LdrRegisterThumbT2
    elif op1 == 0b00 and rn != 0b1111 and (
            (bit_at(instr, 11) and bit_at(instr, 8)) or (substring(instr, 11, 8) == 0b1100)):
        # Load Register
        if (rn == 0b1101 and not bit_at(instr, 10) and bit_at(instr, 9) and
                bit_at(instr, 8) and substring(instr, 7, 0) == 0b00000100):
            return PopThumbT3
        else:
            return LdrImmediateThumbT4
    elif op1 == 0b01 and rn != 0b1111:
        # Load Register
        return LdrImmediateThumbT3
    elif op1 == 0b00 and rn != 0b1111 and substring(instr, 11, 8) == 0b1110:
        # Load Register Unprivileged
        return LdrtT1
    elif not bit_at(instr, 24) and rn == 0b1111:
        # Load Register
        return LdrLiteralT2
