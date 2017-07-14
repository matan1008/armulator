from armulator.armv6.opcodes.abstract_opcodes.usat16 import Usat16
from armulator.armv6.opcodes.opcode import Opcode


class Usat16A1(Usat16, Opcode):
    def __init__(self, instruction, saturate_to, d, n):
        Opcode.__init__(self, instruction)
        Usat16.__init__(self, saturate_to, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        rd = instr[16:20]
        sat_imm = instr[12:16]
        saturate_to = sat_imm.uint + 1
        if rd.uint == 15 or rn.uint == 15:
            print "unpredictable"
        else:
            return Usat16A1(instr, **{"saturate_to": saturate_to, "d": rd.uint, "n": rn.uint})
