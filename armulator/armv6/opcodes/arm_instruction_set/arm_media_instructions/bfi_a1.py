from armulator.armv6.opcodes.abstract_opcodes.bfi import Bfi
from armulator.armv6.opcodes.opcode import Opcode


class BfiA1(Bfi, Opcode):
    def __init__(self, instruction, lsbit, msbit, d, n):
        Opcode.__init__(self, instruction)
        Bfi.__init__(self, lsbit, msbit, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        lsb = instr[20:25]
        rd = instr[16:20]
        msb = instr[11:16]
        if rd.uint == 15:
            print("unpredictable")
        else:
            return BfiA1(instr, **{"lsbit": lsb.uint, "msbit": msb.uint, "d": rd.uint, "n": rn.uint})
