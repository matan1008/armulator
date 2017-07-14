from armulator.armv6.opcodes.abstract_opcodes.smmla import Smmla
from armulator.armv6.opcodes.opcode import Opcode


class SmmlaT1(Smmla, Opcode):
    def __init__(self, instruction, round_, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smmla.__init__(self, round_, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd = instr[20:24]
        ra = instr[16:20]
        rn = instr[12:16]
        round_ = instr[27]
        if rd.uint in (13, 15) or rn.uint in (13, 15) or rm.uint in (13, 15) or ra.uint == 13:
            print "unpredictable"
        else:
            return SmmlaT1(instr, **{"round_": round_, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
