from armulator.opcodes.abstract_opcodes.strexh import Strexh
from armulator.opcodes.opcode import Opcode


class StrexhT1(Strexh, Opcode):
    def __init__(self, instruction, t, d, n):
        Opcode.__init__(self, instruction)
        Strexh.__init__(self, t, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[28:32]
        rt = instr[16:20]
        rn = instr[12:16]
        if rd.uint in (13, 15) or rt.uint in (13, 15) or rn.uint == 15 or rd.uint == rn.uint or rd.uint == rt.uint:
            print "unpredictable"
        else:
            return StrexhT1(instr, **{"t": rt.uint, "d": rd.uint, "n": rn.uint})
