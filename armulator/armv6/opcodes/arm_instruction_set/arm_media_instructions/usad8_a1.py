from armulator.armv6.opcodes.abstract_opcodes.usad8 import Usad8
from armulator.armv6.opcodes.opcode import Opcode


class Usad8A1(Usad8, Opcode):
    def __init__(self, instruction, m, d, n):
        Opcode.__init__(self, instruction)
        Usad8.__init__(self, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        rm = instr[20:24]
        rd = instr[12:16]
        if rd.uint == 15 or rm.uint == 15 or rn.uint == 15:
            print("unpredictable")
        else:
            return Usad8A1(instr, **{"m": rm.uint, "d": rd.uint, "n": rn.uint})
