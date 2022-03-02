from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrd_immediate import LdrdImmediate


class LdrdImmediateA1(LdrdImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        w = bit_at(instr, 21)
        index = bit_at(instr, 24)
        imm4_l = substring(instr, 3, 0)
        imm4_h = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        imm32 = chain(imm4_h, imm4_l, 4)
        t2 = rt + 1
        wback = (not index) or w
        if bit_at(rt, 0) or (not index and w) or (wback and (rn == rt or rn == t2)) or t2 == 15:
            print('unpredictable')
        else:
            return LdrdImmediateA1(instr, add=add, wback=wback, index=index, imm32=imm32, t=rt, t2=t2, n=rn)
