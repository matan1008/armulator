from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.ldrb_literal import LdrbLiteral


class LdrbLiteralA1(LdrbLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        p = bit_at(instr, 24)
        add = bit_at(instr, 23)
        w = bit_at(instr, 21)
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        if p == w or rt == 15:
            print('unpredictable')
        else:
            return LdrbLiteralA1(instr, add=add, imm32=imm32, t=rt)
