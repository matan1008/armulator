from armulator.armv6.opcodes.abstract_opcodes.sxth import Sxth
from armulator.armv6.opcodes.opcode import Opcode


class SxthT2(Sxth, Opcode):
    def __init__(self, instruction, m, d, rotation):
        Opcode.__init__(self, instruction)
        Sxth.__init__(self, m, d, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rotate = instr[26:28]
        rd = instr[20:24]
        rotation = (rotate + "0b000").uint
        if rd.uint in (13, 15) or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return SxthT2(instr, **{"m": rm.uint, "d": rd.uint, "rotation": rotation})
