from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.umaal import Umaal


class UmaalA1(Umaal):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rm = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rd_hi = substring(instr, 19, 16)
        if rd_hi == 15 or rm == 15 or rn == 15 or rd_lo == 15 or (rd_lo == rd_hi):
            print('unpredictable')
        else:
            return UmaalA1(instr, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
