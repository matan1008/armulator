from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strex import Strex


class StrexA1(Strex):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        imm32 = 0
        if rd == 15 or rn == 15 or rt == 15 or rn == rd or rd == rt:
            print('unpredictable')
        else:
            return StrexA1(instr, imm32=imm32, t=rt, d=rd, n=rn)
