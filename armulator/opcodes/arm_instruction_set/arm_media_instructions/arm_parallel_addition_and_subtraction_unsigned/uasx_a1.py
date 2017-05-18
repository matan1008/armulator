from armulator.opcodes.abstract_opcodes.uasx import Uasx
from armulator.opcodes.opcode import Opcode


class UasxA1(Uasx, Opcode):
    def __init__(self, instruction, m, d, n):
        Opcode.__init__(self, instruction)
        Uasx.__init__(self, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[16:20]
        rn = instr[12:16]
        if rd.uint == 15 or rn.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return UasxA1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint})
