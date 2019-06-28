from armulator.armv6.opcodes.abstract_opcodes.ldrexh import Ldrexh
from armulator.armv6.opcodes.opcode import Opcode


class LdrexhT1(Ldrexh, Opcode):
    def __init__(self, instruction, t, n):
        Opcode.__init__(self, instruction)
        Ldrexh.__init__(self, t, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        rn = instr[12:16]
        if rt.uint in (13, 15) or rn.uint == 15:
            print("unpredictable")
        else:
            return LdrexhT1(instr, **{"t": rt.uint, "n": rn.uint})
