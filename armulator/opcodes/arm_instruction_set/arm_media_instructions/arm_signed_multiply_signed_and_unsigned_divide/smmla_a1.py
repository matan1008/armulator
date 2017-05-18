from armulator.opcodes.abstract_opcodes.smmla import Smmla
from armulator.opcodes.opcode import Opcode


class SmmlaA1(Smmla, Opcode):
    def __init__(self, instruction, round_, m, a, d, n):
        Opcode.__init__(self, instruction)
        Smmla.__init__(self, round_, m, a, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        round_ = instr[26]
        rm = instr[20:24]
        ra = instr[16:20]
        rd = instr[12:16]
        if rd.uint == 15 or rn.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return SmmlaA1(instr, **{"round_": round_, "m": rm.uint, "a": ra.uint, "d": rd.uint, "n": rn.uint})
