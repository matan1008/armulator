from armulator.armv6.opcodes.abstract_opcodes.usada8 import Usada8
from armulator.armv6.opcodes.opcode import Opcode


class Usada8T1(Usada8, Opcode):
    def __init__(self, instruction, m, a, d, n):
        Opcode.__init__(self, instruction)
        Usada8.__init__(self, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint == 13:
            print "unpredictable"
        else:
            return Usada8T1(instr, **{"m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
