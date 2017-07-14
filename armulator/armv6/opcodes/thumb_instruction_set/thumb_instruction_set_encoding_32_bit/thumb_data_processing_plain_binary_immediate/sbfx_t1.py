from armulator.armv6.opcodes.abstract_opcodes.sbfx import Sbfx
from armulator.armv6.opcodes.opcode import Opcode


class SbfxT1(Sbfx, Opcode):
    def __init__(self, instruction, lsbit, widthminus1, d, n):
        Opcode.__init__(self, instruction)
        Sbfx.__init__(self, lsbit, widthminus1, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        widthm1 = instr[27:32]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        lsbit = (imm3 + imm2).uint
        if rd.uint in (13, 15) or rn.uint in (13, 15):
            print "unpredictable"
        else:
            return SbfxT1(instr, **{"lsbit": lsbit, "widthminus1": widthm1.uint, "d": rd.uint, "n": rn.uint})
