from armulator.armv6.opcodes.abstract_opcodes.umull import Umull
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.configurations import arch_version


class UmullA1(Umull, Opcode):
    def __init__(self, instruction, setflags, m, d_hi, d_lo, n):
        Opcode.__init__(self, instruction)
        Umull.__init__(self, setflags, m, d_hi, d_lo, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        rm = instr[20:24]
        rd_lo = instr[16:20]
        rd_hi = instr[12:16]
        setflags = instr[11]
        if rd_hi.uint == 15 or rm.uint == 15 or rn.uint == 15 or rd_lo.uint == 15 or (rd_lo.uint == rd_hi.uint) or (
                        arch_version() < 6 and (rd_hi.uint == rn.uint or rd_lo.uint == rn.uint)):
            print("unpredictable")
        else:
            return UmullA1(instr,
                           **{"setflags": setflags, "m": rm.uint, "d_hi": rd_hi.uint, "d_lo": rd_lo.uint, "n": rn.uint})
