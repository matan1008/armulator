from armulator.armv6.opcodes.abstract_opcodes.smmls import Smmls
from armulator.armv6.opcodes.opcode import Opcode


class SmmlsT1(Smmls, Opcode):
    def __init__(self, instruction, round_, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smmls.__init__(self, round_, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        round_ = instr[27]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint in (13, 15):
            print "unpredictable"
        else:
            return SmmlsT1(instr, **{"round_": round_, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
