from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.umull import Umull


class UmullT1(Umull):
    @staticmethod
    def from_bitarray(instr, processor):
        setflags = False
        rm = substring(instr, 3, 0)
        rd_hi = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rm in (13, 15) or rn in (13, 15) or rd_hi in (13, 15) or rd_lo in (13, 15) or rd_hi == rd_lo:
            print('unpredictable')
        else:
            return UmullT1(instr, setflags=setflags, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
