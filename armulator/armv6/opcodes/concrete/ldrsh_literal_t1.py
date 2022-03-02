from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrsh_literal import LdrshLiteral


class LdrshLiteralT1(LdrshLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        add = bit_at(instr, 23)
        if rt == 13:
            print('unpredictable')
        else:
            return LdrshLiteralT1(instr, add=add, imm32=imm32, t=rt)
