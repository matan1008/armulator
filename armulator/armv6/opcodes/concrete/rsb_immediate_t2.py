from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.rsb_immediate import RsbImmediate
from armulator.armv6.shift import thumb_expand_imm


class RsbImmediateT2(RsbImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        setflags = bit_at(instr, 20)
        i = bit_at(instr, 26)
        imm32 = thumb_expand_imm(chain(i, chain(imm3, imm8, 8), 11))
        if rd in (13, 15) or rn in (13, 15):
            print('unpredictable')
        else:
            return RsbImmediateT2(instr, setflags=setflags, d=rd, n=rn, imm32=imm32)
