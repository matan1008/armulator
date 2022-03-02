from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smlalxy import Smlalxy


class SmlalxyA1(Smlalxy):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        n_high = bit_at(instr, 5)
        m_high = bit_at(instr, 6)
        rm = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rd_hi = substring(instr, 19, 16)
        if rm == 15 or rd_hi == 15 or rd_lo == 15 or rn == 15 or rd_hi == rd_lo:
            print('unpredictable')
        else:
            return SmlalxyA1(instr, m_high=m_high, n_high=n_high, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
