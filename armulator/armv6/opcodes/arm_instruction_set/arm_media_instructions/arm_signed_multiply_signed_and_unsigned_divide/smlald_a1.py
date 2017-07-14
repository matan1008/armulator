from armulator.armv6.opcodes.abstract_opcodes.smlald import Smlald
from armulator.armv6.opcodes.opcode import Opcode


class SmlaldA1(Smlald, Opcode):
    def __init__(self, instruction, m_swap, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Smlald.__init__(self, m_swap, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        m_swap = instr[26]
        rm = instr[20:24]
        rd_lo = instr[16:20]
        rd_hi = instr[12:16]
        if rd_lo.uint == 15 or rd_hi.uint == 15 or rn.uint == 15 or rm.uint == 15 or rd_lo.uint == rd_hi.uint:
            print "unpredictable"
        else:
            return SmlaldA1(instr, **{"m_swap": m_swap, "m": rm.uint, "d_hi": rd_hi.uint, "d_lo": rd_lo.uint,
                                      "n": rn.uint})
