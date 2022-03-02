from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrh_literal import LdrhLiteral


class LdrhLiteralT1(LdrhLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        if rt == 13:
            print('unpredictable')
        else:
            return LdrhLiteralT1(instr, add=add, imm32=imm32, t=rt)
