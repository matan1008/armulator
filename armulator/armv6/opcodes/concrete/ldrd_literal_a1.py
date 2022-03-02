from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrd_literal import LdrdLiteral


class LdrdLiteralA1(LdrdLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm4_l = substring(instr, 3, 0)
        imm4_h = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        imm32 = chain(imm4_h, imm4_l, 4)
        t2 = rt + 1
        if bit_at(rt, 0) or t2 == 15:
            print('unpredictable')
        else:
            return LdrdLiteralA1(instr, add=add, imm32=imm32, t=rt, t2=t2)
