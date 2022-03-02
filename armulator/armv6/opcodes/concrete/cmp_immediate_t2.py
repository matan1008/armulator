from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.cmp_immediate import CmpImmediate
from armulator.armv6.shift import thumb_expand_imm


class CmpImmediateT2(CmpImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        i = bit_at(instr, 26)
        imm32 = thumb_expand_imm(chain(i, chain(imm3, imm8, 8), 11))
        if rn == 15:
            print('unpredictable')
        else:
            return CmpImmediateT2(instr, n=rn, imm32=imm32)
