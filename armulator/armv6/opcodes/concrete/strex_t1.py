from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strex import Strex


class StrexT1(Strex):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        imm32 = imm8 << 2
        if rd in (13, 15) or rt in (13, 15) or rn == 15 or rd == rn or rd == rt:
            print('unpredictable')
        else:
            return StrexT1(instr, imm32=imm32, t=rt, d=rd, n=rn)
