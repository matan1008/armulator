from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrd_immediate import LdrdImmediate


class LdrdImmediateT1(LdrdImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rt2 = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = bit_at(instr, 24)
        add = bit_at(instr, 23)
        wback = bit_at(instr, 21)
        imm32 = imm8 << 2
        if (wback and (rn == rt or rn == rt2)) or rt == rt2 or rt in (13, 15) or rt2 in (13, 15):
            print('unpredictable')
        else:
            return LdrdImmediateT1(instr, add=add, wback=wback, index=index, imm32=imm32, t=rt, t2=rt2, n=rn)
