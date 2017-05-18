from armulator.opcodes.abstract_opcodes.smlaw import Smlaw
from armulator.opcodes.opcode import Opcode


class SmlawT1(Smlaw, Opcode):
    def __init__(self, instruction, m_high, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smlaw.__init__(self, m_high, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        m_high = instr[27]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint == 13:
            print "unpredictable"
        else:
            return SmlawT1(instr, **{"m_high": m_high, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
