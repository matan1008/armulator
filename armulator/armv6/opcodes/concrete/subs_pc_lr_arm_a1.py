from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_arm import SubsPcLrArm
from armulator.armv6.shift import arm_expand_imm


class SubsPcLrArmA1(SubsPcLrArm):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rn = substring(instr, 19, 16)
        opcode = substring(instr, 24, 21)
        imm32 = arm_expand_imm(imm12)
        return SubsPcLrArmA1(instr, register_form=False, n=rn, opcode=opcode, imm32=imm32)
