from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.strexd import Strexd


class StrexdA1(Strexd):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 3, 0)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        t2 = rt + 1
        if rn == 15 or rd == 15 or bit_at(rt, 0) or rt == 14 or rn == rd or rt == rd or t2 == rd:
            print('unpredictable')
        else:
            return StrexdA1(instr, t=rt, t2=t2, d=rd, n=rn)
