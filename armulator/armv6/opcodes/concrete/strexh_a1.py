from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strexh import Strexh


class StrexhA1(Strexh):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rt == 15 or rn == rd or rd == rt:
            print('unpredictable')
        else:
            return StrexhA1(instr, t=rt, d=rd, n=rn)
