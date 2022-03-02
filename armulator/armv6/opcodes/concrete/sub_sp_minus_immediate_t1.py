from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate


class SubSpMinusImmediateT1(SubSpMinusImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm7 = substring(instr, 6, 0)
        setflags = False
        d = 13
        imm32 = imm7 << 2
        return SubSpMinusImmediateT1(instr, setflags=setflags, d=d, imm32=imm32)
