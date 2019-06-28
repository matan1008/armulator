from armulator.armv6.opcodes.abstract_opcodes.sbfx import Sbfx
from armulator.armv6.opcodes.opcode import Opcode


class SbfxA1(Sbfx, Opcode):
    def __init__(self, instruction, lsbit, widthminus1, d, n):
        Opcode.__init__(self, instruction)
        Sbfx.__init__(self, lsbit, widthminus1, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        lsb = instr[20:25]
        rd = instr[16:20]
        widthm1 = instr[11:16]
        if rd.uint == 15 or rn.uint == 15:
            print("unpredictable")
        else:
            return SbfxA1(instr, **{"lsbit": lsb.uint, "widthminus1": widthm1.uint, "d": rd.uint, "n": rn.uint})
