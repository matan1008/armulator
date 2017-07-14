from armulator.armv6.opcodes.abstract_opcodes.mcrr import Mcrr
from armulator.armv6.opcodes.opcode import Opcode


class McrrA1(Mcrr, Opcode):
    def __init__(self, instruction, cp, t, t2):
        Opcode.__init__(self, instruction)
        Mcrr.__init__(self, cp, t, t2)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        rt2 = instr[12:16]
        if rt.uint == 15 or rt2.uint == 15:
            print "unpredictable"
        else:
            return McrrA1(instr, **{"cp": coproc.uint, "t": rt.uint, "t2": rt2.uint})
