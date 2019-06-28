from armulator.armv6.opcodes.abstract_opcodes.strexd import Strexd
from armulator.armv6.opcodes.opcode import Opcode


class StrexdA1(Strexd, Opcode):
    def __init__(self, instruction, t, t2, d, n):
        Opcode.__init__(self, instruction)
        Strexd.__init__(self, t, t2, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[-4:]
        rd = instr[16:20]
        rn = instr[12:16]
        t2 = rt.uint + 1
        if (rn.uint == 15 or rd.uint == 15 or rt[3] or rt.uint == 14 or
                rn.uint == rd.uint or rt.uint == rd.uint or t2 == rd.uint):
            print("unpredictable")
        else:
            return StrexdA1(instr, **{"t": rt.uint, "t2": t2, "d": rd.uint, "n": rn.uint})
