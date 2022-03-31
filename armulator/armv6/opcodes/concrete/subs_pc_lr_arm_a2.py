from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.subs_pc_lr_arm import SubsPcLrArm
from armulator.armv6.shift import decode_imm_shift


class SubsPcLrArmA2(SubsPcLrArm):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        imm5 = substring(instr, 11, 7)
        rn = substring(instr, 19, 16)
        opcode = substring(instr, 24, 21)
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return SubsPcLrArmA2(instr, register_form=True, n=rn, opcode=opcode, m=rm, shift_t=shift_t, shift_n=shift_n)
