from armulator.armv6.opcodes.abstract_opcodes.uhsub8 import Uhsub8
from armulator.armv6.opcodes.opcode import Opcode


class Uhsub8T1(Uhsub8, Opcode):
    def __init__(self, instruction, m, d, n):
        Opcode.__init__(self, instruction)
        Uhsub8.__init__(self, m, d, n)

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
            return Uhsub8T1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint})
