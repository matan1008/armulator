from armulator.opcodes.abstract_opcodes.strex import Strex
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zeros


class StrexA1(Strex, Opcode):
    def __init__(self, instruction, imm32, t, d, n):
        Opcode.__init__(self, instruction)
        Strex.__init__(self, imm32, t, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[-4:]
        rd = instr[16:20]
        rn = instr[12:16]
        imm32 = zeros(32)
        if rd.uint == 15 or rn.uint == 15 or rt.uint == 15 or rn.uint == rd.uint or rd.uint == rt.uint:
            print "unpredictable"
        else:
            return StrexA1(instr, **{"imm32": imm32, "t": rt.uint, "d": rd.uint, "n": rn.uint})
