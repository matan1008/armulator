from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smlsld import Smlsld


class SmlsldT1(Smlsld):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd_hi = substring(instr, 11, 8)
        rd_lo = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        m_swap = bit_at(instr, 4)
        if rm in (13, 15) or rn in (13, 15) or rd_hi in (13, 15) or rd_lo in (
                13, 15) or rd_hi == rd_lo:
            print('unpredictable')
        else:
            return SmlsldT1(instr, m_swap=m_swap, m=rm, d_hi=rd_hi, d_lo=rd_lo, n=rn)
