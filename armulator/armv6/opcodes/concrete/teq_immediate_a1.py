from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.teq_immediate import TeqImmediate
from armulator.armv6.shift import arm_expand_imm_c


class TeqImmediateA1(TeqImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rn = substring(instr, 19, 16)
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.c)
        return TeqImmediateA1(instr, n=rn, imm32=imm32, carry=carry)
