from armulator.armv6.opcodes.abstract_opcodes.smla import Smla
from armulator.armv6.opcodes.opcode import Opcode


class SmlaA1(Smla, Opcode):
    def __init__(self, instruction, m_high, n_high, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smla.__init__(self, m_high, n_high, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        n_high = instr[26]
        m_high = instr[25]
        rm = instr[20:24]
        ra = instr[16:20]
        rd = instr[12:16]
        if rm.uint == 15 or ra.uint == 15 or rd.uint == 15 or rn.uint == 15:
            print "unpredictable"
        else:
            return SmlaA1(instr, **{"m_high": m_high, "n_high": n_high, "m": rm.uint, "a": ra.uint, "d": rd.uint,
                                    "n": rn.uint})
