from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrd_literal import LdrdLiteral


class LdrdLiteralT1(LdrdLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rt2 = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        imm32 = imm8 << 2
        if rt == rt2 or rt in (13, 15) or rt2 in (13, 15) or bit_at(instr, 21):
            print('unpredictable')
        else:
            return LdrdLiteralT1(instr, add=add, imm32=imm32, t=rt, t2=rt2)
