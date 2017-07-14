from armulator.armv6.opcodes.abstract_opcodes.smul import Smul
from armulator.armv6.opcodes.opcode import Opcode


class SmulT1(Smul, Opcode):
    def __init__(self, instruction, m_high, n_high, m, d, n):
        Opcode.__init__(self, instruction)
        Smul.__init__(self, m_high, n_high, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        rn = instr[12:16]
        m_high = instr[27]
        n_high = instr[26]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return SmulT1(instr, **{"m_high": m_high, "n_high": n_high, "m": rm.uint, "d": rd.uint, "n": rn.uint})
