from armulator.armv6.opcodes.abstract_opcodes.smlaw import Smlaw
from armulator.armv6.opcodes.opcode import Opcode


class SmlawA1(Smlaw, Opcode):
    def __init__(self, instruction, m_high, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smlaw.__init__(self, m_high, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        m_high = instr[25]
        rm = instr[20:24]
        ra = instr[16:20]
        rd = instr[12:16]
        if rm.uint == 15 or ra.uint == 15 or rd.uint == 15 or rn.uint == 15:
            print("unpredictable")
        else:
            return SmlawA1(instr, **{"m_high": m_high, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
