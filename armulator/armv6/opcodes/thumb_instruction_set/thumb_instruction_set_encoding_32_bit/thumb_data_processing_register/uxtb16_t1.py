from armulator.armv6.opcodes.abstract_opcodes.uxtb16 import Uxtb16
from armulator.armv6.opcodes.opcode import Opcode


class Uxtb16T1(Uxtb16, Opcode):
    def __init__(self, instruction, m, d, rotation):
        Opcode.__init__(self, instruction)
        Uxtb16.__init__(self, m, d, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rotate = instr[26:28]
        rd = instr[20:24]
        rotation = (rotate + "0b000").uint
        if rd.uint in (13, 15) or rm.uint in (13, 15):
            print("unpredictable")
        else:
            return Uxtb16T1(instr, **{"m": rm.uint, "d": rd.uint, "rotation": rotation})
