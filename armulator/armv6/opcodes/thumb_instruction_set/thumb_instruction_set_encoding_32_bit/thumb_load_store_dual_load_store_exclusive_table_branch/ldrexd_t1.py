from armulator.armv6.opcodes.abstract_opcodes.ldrexd import Ldrexd
from armulator.armv6.opcodes.opcode import Opcode


class LdrexdT1(Ldrexd, Opcode):
    def __init__(self, instruction, t, t2, n):
        Opcode.__init__(self, instruction)
        Ldrexd.__init__(self, t, t2, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt2 = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        if rt.uint in (13, 15) or rt2.uint in (13, 15) or rn.uint == 15 or rt2.uint == rt.uint:
            print "unpredictable"
        else:
            return LdrexdT1(instr, **{"t": rt.uint, "t2": rt2.uint, "n": rn.uint})
