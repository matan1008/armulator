from armulator.opcodes.abstract_opcodes.mcr import Mcr
from armulator.opcodes.opcode import Opcode


class McrA1(Mcr, Opcode):
    def __init__(self, instruction, cp, t):
        Opcode.__init__(self, instruction)
        Mcr.__init__(self, cp, t)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        coproc = instr[20:24]
        rt = instr[16:20]
        if rt.uint == 15:
            print "unpredictable"
        else:
            return McrA1(instr, **{"cp": coproc.uint, "t": rt.uint})
