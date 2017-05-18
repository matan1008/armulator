from armulator.opcodes.abstract_opcodes.sxtb import Sxtb
from armulator.opcodes.opcode import Opcode


class SxtbT1(Sxtb, Opcode):
    def __init__(self, instruction, m, d, rotation):
        Opcode.__init__(self, instruction)
        Sxtb.__init__(self, m, d, rotation)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rd = instr[13:16]
        rm = instr[10:13]
        rotation = 0
        return SxtbT1(instr, **{"m": rm.uint, "d": rd.uint, "rotation": rotation})
