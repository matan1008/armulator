from armulator.armv6.opcodes.abstract_opcodes.ldrexd import Ldrexd
from armulator.armv6.opcodes.opcode import Opcode


class LdrexdA1(Ldrexd, Opcode):
    def __init__(self, instruction, t, t2, n):
        Opcode.__init__(self, instruction)
        Ldrexd.__init__(self, t, t2, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        rn = instr[12:16]
        t2 = rt.uint + 1
        if rn.uint == 15 or rt[3] or rt.uint == 14:
            print("unpredictable")
        else:
            return LdrexdA1(instr, **{"t": rt.uint, "t2": t2, "n": rn.uint})
