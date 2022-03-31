from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.pld_literal import PldLiteral


class PldLiteralT1(PldLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        add = bit_at(instr, 23)
        return PldLiteralT1(instr, add=add, imm32=imm32)
