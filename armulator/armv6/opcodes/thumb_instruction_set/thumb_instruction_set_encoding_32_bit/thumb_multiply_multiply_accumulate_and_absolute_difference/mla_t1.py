from armulator.armv6.opcodes.abstract_opcodes.mla import Mla
from armulator.armv6.opcodes.opcode import Opcode


class MlaT1(Mla, Opcode):
    def __init__(self, instruction, setflags, m, a, d, n):
        Opcode.__init__(self, instruction)
        Mla.__init__(self, setflags, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        setflags = False
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint == 13:
            print("unpredictable")
        else:
            return MlaT1(instr, **{"setflags": setflags, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
