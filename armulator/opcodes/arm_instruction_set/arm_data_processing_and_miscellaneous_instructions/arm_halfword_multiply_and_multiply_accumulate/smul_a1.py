from armulator.opcodes.abstract_opcodes.smul import Smul
from armulator.opcodes.opcode import Opcode


class SmulA1(Smul, Opcode):
    def __init__(self, instruction, m_high, n_high, m, d, n):
        Opcode.__init__(self, instruction)
        Smul.__init__(self, m_high, n_high, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        n_high = instr[26]
        m_high = instr[25]
        rm = instr[20:24]
        rd = instr[12:16]
        if rm.uint == 15 or rd.uint == 15 or rn.uint == 15:
            print "unpredictable"
        else:
            return SmulA1(instr, **{"m_high": m_high, "n_high": n_high, "m": rm.uint, "d": rd.uint, "n": rn.uint})
