from armulator.opcodes.abstract_opcodes.smlalxy import Smlalxy
from armulator.opcodes.opcode import Opcode


class SmlalxyT1(Smlalxy, Opcode):
    def __init__(self, instruction, m_high, n_high, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Smlalxy.__init__(self, m_high, n_high, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd_hi = instr[20:24]
        rd_lo = instr[16:20]
        rn = instr[12:16]
        m_high = instr[27]
        n_high = instr[26]
        if (rm.uint in (13, 15) or
                rn.uint in (13, 15) or
                rd_hi.uint in (13, 15) or
                rd_lo.uint in (13, 15) or
                rd_hi.uint == rd_lo.uint):
            print "unpredictable"
        else:
            return SmlalxyT1(instr, **{"m_high": m_high, "n_high": n_high, "m": rm.uint, "d_hi": rd_hi.uint,
                                       "d_lo": rd_lo.uint, "n": rn.uint})
