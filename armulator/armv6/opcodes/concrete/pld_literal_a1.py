from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pld_literal import PldLiteral


class PldLiteralA1(PldLiteral):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        add = bit_at(instr, 23)
        return PldLiteralA1(instr, add=add, imm32=imm32)
