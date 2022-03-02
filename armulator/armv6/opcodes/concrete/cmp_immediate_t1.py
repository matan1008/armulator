from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cmp_immediate import CmpImmediate


class CmpImmediateT1(CmpImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 10, 8)
        imm8 = substring(instr, 7, 0)
        return CmpImmediateT1(instr, n=rn, imm32=imm8)
