from armulator.armv6.opcodes.abstract_opcodes.smlalxy import Smlalxy
from armulator.armv6.opcodes.opcode import Opcode


class SmlalxyA1(Smlalxy, Opcode):
    def __init__(self, instruction, m_high, n_high, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Smlalxy.__init__(self, m_high, n_high, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        n_high = instr[26]
        m_high = instr[25]
        rm = instr[20:24]
        rd_lo = instr[16:20]
        rd_hi = instr[12:16]
        if rm.uint == 15 or rd_hi.uint == 15 or rd_lo.uint == 15 or rn.uint == 15 or rd_hi.uint == rd_lo.uint:
            print "unpredictable"
        else:
            return SmlalxyA1(instr, **{"m_high": m_high, "n_high": n_high, "m": rm.uint, "d_hi": rd_hi.uint,
                                       "d_lo": rd_lo.uint, "n": rn.uint})
