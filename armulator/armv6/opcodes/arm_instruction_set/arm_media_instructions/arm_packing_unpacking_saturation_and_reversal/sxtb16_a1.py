from armulator.armv6.opcodes.abstract_opcodes.sxtb16 import Sxtb16
from armulator.armv6.opcodes.opcode import Opcode


class Sxtb16A1(Sxtb16, Opcode):
    def __init__(self, instruction, m, d, rotation):
        Opcode.__init__(self, instruction)
        Sxtb16.__init__(self, m, d, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rotate = instr[20:22]
        rd = instr[16:20]
        rotation = rotate.uint * 8
        if rd.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return Sxtb16A1(instr, **{"m": rm.uint, "d": rd.uint, "rotation": rotation})
