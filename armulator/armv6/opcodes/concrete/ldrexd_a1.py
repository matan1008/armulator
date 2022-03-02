from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrexd import Ldrexd


class LdrexdA1(Ldrexd):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        t2 = rt + 1
        if rn == 15 or bit_at(rt, 0) or rt == 14:
            print('unpredictable')
        else:
            return LdrexdA1(instr, t=rt, t2=t2, n=rn)
