from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.umull import Umull


class UmullA1(Umull):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rm = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rd_hi = substring(instr, 19, 16)
        setflags = bit_at(instr, 20)
        if rd_hi == 15 or rm == 15 or rn == 15 or rd_lo == 15 or (rd_lo == rd_hi) or (
                arch_version() < 6 and (rd_hi == rn or rd_lo == rn)):
            print('unpredictable')
        else:
            return UmullA1(instr, setflags=setflags, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
