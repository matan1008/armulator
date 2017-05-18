from armulator.opcodes.abstract_opcodes.qsax import Qsax
from armulator.opcodes.opcode import Opcode


class QsaxA1(Qsax, Opcode):
    def __init__(self, instruction, m, d, n):
        Opcode.__init__(self, instruction)
        Qsax.__init__(self, m, d, n)

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
            return QsaxA1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint})
