from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.ldr_literal import LdrLiteral


class LdrLiteralA1(LdrLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        index = bit_at(instr, 24)
        add = bit_at(instr, 23)
        w = bit_at(instr, 21)
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        if index == w:
            print('unpredictable')
        else:
            return LdrLiteralA1(instr, add=add, imm32=imm32, t=rt)
