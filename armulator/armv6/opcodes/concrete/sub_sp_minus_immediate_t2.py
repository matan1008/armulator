from armulator.armv6.bits_ops import bit_at, substring, chain
from armulator.armv6.opcodes.abstract_opcodes.sub_sp_minus_immediate import SubSpMinusImmediate
from armulator.armv6.shift import thumb_expand_imm


class SubSpMinusImmediateT2(SubSpMinusImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        setflags = bit_at(instr, 20)
        i = bit_at(instr, 26)
        imm32 = thumb_expand_imm(chain(i, chain(imm3, imm8, 8), 11))
        if rd == 15 and not setflags:
            print('unpredictable')
        else:
            return SubSpMinusImmediateT2(instr, setflags=setflags, d=rd, imm32=imm32)
