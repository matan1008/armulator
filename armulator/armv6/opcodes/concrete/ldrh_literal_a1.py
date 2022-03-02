from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrh_literal import LdrhLiteral


class LdrhLiteralA1(LdrhLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        w = bit_at(instr, 21)
        p = bit_at(instr, 24)
        imm4_l = substring(instr, 3, 0)
        imm4_h = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        imm32 = chain(imm4_h, imm4_l, 4)
        if p == w or rt == 15:
            print('unpredictable')
        else:
            return LdrhLiteralA1(instr, add=add, imm32=imm32, t=rt)
