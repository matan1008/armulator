from armulator.armv6.opcodes.abstract_opcodes.smmul import Smmul
from armulator.armv6.opcodes.opcode import Opcode


class SmmulA1(Smmul, Opcode):
    def __init__(self, instruction, round_, m, d, n):
        Opcode.__init__(self, instruction)
        Smmul.__init__(self, round_, m, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[28:32]
        round_ = instr[26]
        rm = instr[20:24]
        rd = instr[12:16]
        if rd.uint == 15 or rn.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return SmmulA1(instr, **{"round_": round_, "m": rm.uint, "d": rd.uint, "n": rn.uint})
