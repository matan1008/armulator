from armulator.opcodes.abstract_opcodes.smlsld import Smlsld
from armulator.opcodes.opcode import Opcode


class SmlsldT1(Smlsld, Opcode):
    def __init__(self, instruction, m_swap, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Smlsld.__init__(self, m_swap, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd_hi = instr[20:24]
        rd_lo = instr[16:20]
        rn = instr[12:16]
        m_swap = instr[27]
        if rm.uint in (13, 15) or rn.uint in (13, 15) or rd_hi.uint in (13, 15) or rd_lo.uint in (
                13, 15) or rd_hi.uint == rd_lo.uint:
            print "unpredictable"
        else:
            return SmlsldT1(instr, **{"m_swap": m_swap, "m": rm.uint, "d_hi": rd_hi.uint, "d_lo": rd_lo.uint,
                                      "n": rn.uint})
