from armulator.opcodes.abstract_opcodes.qsub16 import Qsub16
from armulator.opcodes.opcode import Opcode


class Qsub16T1(Qsub16, Opcode):
    def __init__(self, instruction, m, d, n):
        Opcode.__init__(self, instruction)
        Qsub16.__init__(self, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        rn = instr[12:16]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return Qsub16T1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint})
