from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.sub_immediate_arm import SubImmediateArm
from armulator.armv6.shift import arm_expand_imm_c


class SubImmediateArmA1(SubImmediateArm):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        setflags = bit_at(instr, 20)
        imm32, carry = arm_expand_imm_c(imm12, processor.registers.cpsr.c)
        return SubImmediateArmA1(instr, setflags=setflags, d=rd, n=rn, imm32=imm32)
