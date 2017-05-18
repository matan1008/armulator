from armulator.opcodes.abstract_opcodes.umaal import Umaal
from armulator.opcodes.opcode import Opcode


class UmaalT1(Umaal, Opcode):
    def __init__(self, instruction, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Umaal.__init__(self, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        rd_hi = instr[20:24]
        rd_lo = instr[16:20]
        rn = instr[12:16]
        if (rm.uint in (13, 15) or
                rn.uint in (13, 15) or
                rd_hi.uint in (13, 15) or
                rd_lo.uint in (13, 15) or
                rd_hi.uint == rd_lo.uint):
            print "unpredictable"
        else:
            return UmaalT1(instr, **{"m": rm.uint, "d_hi": rd_hi.uint, "d_lo": rd_lo.uint, "n": rn.uint})
