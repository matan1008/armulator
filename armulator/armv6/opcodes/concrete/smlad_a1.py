from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.smlad import Smlad


class SmladA1(Smlad):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        m_swap = bit_at(instr, 5)
        rm = substring(instr, 11, 8)
        ra = substring(instr, 15, 12)
        rd = substring(instr, 19, 16)
        if rd == 15 or rn == 15 or rm == 15:
            print('unpredictable')
        else:
            return SmladA1(instr, m_swap=m_swap, m=rm, a=ra, d=rd, n=rn)
