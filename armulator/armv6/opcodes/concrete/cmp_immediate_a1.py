from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.cmp_immediate import CmpImmediate
from armulator.armv6.shift import arm_expand_imm


class CmpImmediateA1(CmpImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rn = substring(instr, 19, 16)
        imm32 = arm_expand_imm(imm12)
        return CmpImmediateA1(instr, n=rn, imm32=imm32)
