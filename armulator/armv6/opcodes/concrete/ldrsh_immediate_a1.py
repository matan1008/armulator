from armulator.armv6.bits_ops import bit_at, substring, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrsh_immediate import LdrshImmediate


class LdrshImmediateA1(LdrshImmediate):
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
        wback = (not index) or w
        if rt == 15 or (wback and rn == rt):
            print('unpredictable')
        else:
            return LdrshImmediateA1(instr, add=add, wback=wback, index=index, imm32=imm32, t=rt, n=rn)
