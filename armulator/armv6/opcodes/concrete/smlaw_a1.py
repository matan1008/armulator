from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smlaw import Smlaw


class SmlawA1(Smlaw):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        m_high = bit_at(instr, 6)
        rm = substring(instr, 11, 8)
        ra = substring(instr, 15, 12)
        rd = substring(instr, 19, 16)
        if rm == 15 or ra == 15 or rd == 15 or rn == 15:
            print('unpredictable')
        else:
            return SmlawA1(instr, m_high=m_high, m=rm, a=ra, d=rd, n=rn)
