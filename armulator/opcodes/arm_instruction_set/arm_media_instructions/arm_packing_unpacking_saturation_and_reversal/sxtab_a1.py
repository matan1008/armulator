from armulator.opcodes.abstract_opcodes.sxtab import Sxtab
from armulator.opcodes.opcode import Opcode


class SxtabA1(Sxtab, Opcode):
    def __init__(self, instruction, m, d, n, rotation):
        Opcode.__init__(self, instruction)
        Sxtab.__init__(self, m, d, n, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rotate = instr[20:22]
        rd = instr[16:20]
        rn = instr[12:16]
        rotation = rotate.uint * 8
        if rd.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return SxtabA1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint, "rotation": rotation})
