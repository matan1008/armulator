from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldr_literal import LdrLiteral


class LdrLiteralT1(LdrLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rt = substring(instr, 10, 8)
        add = True
        imm32 = imm8 << 2
        return LdrLiteralT1(instr, add=add, imm32=imm32, t=rt)
