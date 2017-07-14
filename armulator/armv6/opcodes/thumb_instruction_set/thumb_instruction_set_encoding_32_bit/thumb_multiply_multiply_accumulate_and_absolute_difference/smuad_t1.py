from armulator.armv6.opcodes.abstract_opcodes.smuad import Smuad
from armulator.armv6.opcodes.opcode import Opcode


class SmuadT1(Smuad, Opcode):
    def __init__(self, instruction, m_swap, m, d, n):
        Opcode.__init__(self, instruction)
        Smuad.__init__(self, m_swap, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        rn = instr[12:16]
        m_swap = instr[27]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return SmuadT1(instr, **{"m_swap": m_swap, "m": rm.uint, "d": rd.uint, "n": rn.uint})
