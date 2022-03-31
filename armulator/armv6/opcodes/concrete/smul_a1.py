from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.smul import Smul


class SmulA1(Smul):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        n_high = bit_at(instr, 5)
        m_high = bit_at(instr, 6)
        rm = substring(instr, 11, 8)
        rd = substring(instr, 19, 16)
        if rm == 15 or rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return SmulA1(instr, m_high=m_high, n_high=n_high, m=rm, d=rd, n=rn)
