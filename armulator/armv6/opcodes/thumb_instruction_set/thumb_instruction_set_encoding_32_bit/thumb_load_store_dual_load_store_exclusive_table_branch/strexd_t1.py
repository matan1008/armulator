from armulator.armv6.opcodes.abstract_opcodes.strexd import Strexd
from armulator.armv6.opcodes.opcode import Opcode


class StrexdT1(Strexd, Opcode):
    def __init__(self, instruction, t, t2, d, n):
        Opcode.__init__(self, instruction)
        Strexd.__init__(self, t, t2, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[28:32]
        rt2 = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        if rd.uint in (13, 15) or rt.uint in (13, 15) or rt2.uint in (
                13, 15) or rn.uint == 15 or rd.uint == rn.uint or rd.uint == rt.uint or rd.uint == rt2.uint:
            print "unpredictable"
        else:
            return StrexdT1(instr, **{"t": rt.uint, "t2": rt2.uint, "d": rd.uint, "n": rn.uint})
