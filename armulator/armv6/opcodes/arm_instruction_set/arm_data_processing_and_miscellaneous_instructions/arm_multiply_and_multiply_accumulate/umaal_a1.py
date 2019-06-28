from armulator.armv6.opcodes.abstract_opcodes.umaal import Umaal
from armulator.armv6.opcodes.opcode import Opcode


class UmaalA1(Umaal, Opcode):
    def __init__(self, instruction, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Umaal.__init__(self, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        rm = instr[20:24]
        rd_lo = instr[16:20]
        rd_hi = instr[12:16]
        if rd_hi.uint == 15 or rm.uint == 15 or rn.uint == 15 or rd_lo.uint == 15 or (rd_lo.uint == rd_hi.uint):
            print("unpredictable")
        else:
            return UmaalA1(instr, **{"m": rm.uint, "d_hi": rd_hi.uint, "d_lo": rd_lo.uint, "n": rn.uint})
