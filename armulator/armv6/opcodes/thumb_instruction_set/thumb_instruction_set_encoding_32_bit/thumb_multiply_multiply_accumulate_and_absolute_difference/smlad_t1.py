from armulator.armv6.opcodes.abstract_opcodes.smlad import Smlad
from armulator.armv6.opcodes.opcode import Opcode


class SmladT1(Smlad, Opcode):
    def __init__(self, instruction, m_swap, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smlad.__init__(self, m_swap, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        m_swap = instr[27]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint == 13:
            print("unpredictable")
        else:
            return SmladT1(instr, **{"m_swap": m_swap, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
