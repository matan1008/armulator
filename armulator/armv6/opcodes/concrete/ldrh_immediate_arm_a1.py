from armulator.armv6.bits_ops import bit_at, substring, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrh_immediate_arm import LdrhImmediateArm


class LdrhImmediateArmA1(LdrhImmediateArm):
    @staticmethod
    def from_bitarray(instr, processor):
        w = bit_at(instr, 21)
        p = bit_at(instr, 24)
        imm4_l = substring(instr, 3, 0)
        imm4_h = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        imm32 = chain(imm4_h, imm4_l, 4)
        wback = (not p) or w
        if rt == 15 or (wback and (rn == 15 or rn == rt)):
            print('unpredictable')
        else:
            return LdrhImmediateArmA1(instr, add=add, wback=wback, index=p, imm32=imm32, t=rt, n=rn)
