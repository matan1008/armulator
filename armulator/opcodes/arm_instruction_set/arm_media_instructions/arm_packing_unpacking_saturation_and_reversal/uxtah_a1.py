from armulator.opcodes.abstract_opcodes.uxtah import Uxtah
from armulator.opcodes.opcode import Opcode


class UxtahA1(Uxtah, Opcode):
    def __init__(self, instruction, m, d, n, rotation):
        Opcode.__init__(self, instruction)
        Uxtah.__init__(self, m, d, n, rotation)

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
            return UxtahA1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint, "rotation": rotation})
