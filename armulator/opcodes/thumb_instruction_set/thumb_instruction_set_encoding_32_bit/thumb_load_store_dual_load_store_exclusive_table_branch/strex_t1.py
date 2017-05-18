from armulator.opcodes.abstract_opcodes.strex import Strex
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class StrexT1(Strex, Opcode):
    def __init__(self, instruction, imm32, t, d, n):
        Opcode.__init__(self, instruction)
        Strex.__init__(self, imm32, t, d, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        rt = instr[16:20]
        rn = instr[12:16]
        imm32 = zero_extend(imm8 + "0b00", 32)
        if rd.uint in (13, 15) or rt.uint in (13, 15) or rn.uint == 15 or rd.uint == rn.uint or rd.uint == rt.uint:
            print "unpredictable"
        else:
            return StrexT1(instr, **{"imm32": imm32, "t": rt.uint, "d": rd.uint, "n": rn.uint})
