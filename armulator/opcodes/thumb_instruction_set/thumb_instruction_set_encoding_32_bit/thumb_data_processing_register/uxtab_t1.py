from armulator.opcodes.abstract_opcodes.uxtab import Uxtab
from armulator.opcodes.opcode import Opcode


class UxtabT1(Uxtab, Opcode):
    def __init__(self, instruction, m, d, n, rotation):
        Opcode.__init__(self, instruction)
        Uxtab.__init__(self, m, d, n, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rotate = instr[26:28]
        rd = instr[20:24]
        rn = instr[12:16]
        rotation = (rotate + "0b000").uint
        if rd.uint in (13, 15) or rn.uint == 13 or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return UxtabT1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint, "rotation": rotation})
