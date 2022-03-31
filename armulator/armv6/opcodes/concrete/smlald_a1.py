from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smlald import Smlald


class SmlaldA1(Smlald):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        m_swap = bit_at(instr, 5)
        rm = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rd_hi = substring(instr, 19, 16)
        if rd_lo == 15 or rd_hi == 15 or rn == 15 or rm == 15 or rd_lo == rd_hi:
            print('unpredictable')
        else:
            return SmlaldA1(instr, m_swap=m_swap, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
