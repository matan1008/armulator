from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.smla_a1 import SmlaA1
from armulator.armv6.opcodes.concrete.smlalxy_a1 import SmlalxyA1
from armulator.armv6.opcodes.concrete.smlaw_a1 import SmlawA1
from armulator.armv6.opcodes.concrete.smul_a1 import SmulA1
from armulator.armv6.opcodes.concrete.smulw_a1 import SmulwA1


def decode_instruction(instr):
    op1 = substring(instr, 22, 21)
    op = bit_at(instr, 5)
    if op1 == 0b00:
        # Signed 16-bit multiply, 32-bit accumulate
        return SmlaA1
    elif op1 == 0b01 and not op:
        # Signed 16-bit X 32-bit multiply, 32-bit accumulate
        return SmlawA1
    elif op1 == 0b01 and op:
        # Signed 16-bit X 32-bit multiply, 32-bit result
        return SmulwA1
    elif op1 == 0b10:
        # Signed 16-bit multiply, 64-bit accumulate
        return SmlalxyA1
    elif op1 == 0b11:
        # Signed 16-bit multiply, 64-bit result
        return SmulA1
