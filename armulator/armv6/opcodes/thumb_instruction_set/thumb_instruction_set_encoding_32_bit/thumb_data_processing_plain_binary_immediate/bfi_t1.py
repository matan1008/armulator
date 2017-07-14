from armulator.armv6.opcodes.abstract_opcodes.bfi import Bfi
from armulator.armv6.opcodes.opcode import Opcode


class BfiT1(Bfi, Opcode):
    def __init__(self, instruction, lsbit, msbit, d, n):
        Opcode.__init__(self, instruction)
        Bfi.__init__(self, lsbit, msbit, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        msb = instr[27:32]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        lsbit = (imm3 + imm2).uint
        if rd.uint in (13, 15) or rn.uint == 13:
            print "unpredictable"
        else:
            return BfiT1(instr, **{"lsbit": lsbit, "msbit": msb.uint, "d": rd.uint, "n": rn.uint})
