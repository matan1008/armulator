from armulator.opcodes.abstract_opcodes.ldrd_literal import LdrdLiteral
from armulator.opcodes.opcode import Opcode


class LdrdLiteralA1(LdrdLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t, t2):
        Opcode.__init__(self, instruction)
        LdrdLiteral.__init__(self, add, imm32, t, t2)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm4_l = instr[-4:]
        imm4_h = instr[20:24]
        rt = instr[16:20]
        add = instr[8]
        imm32 = "0b000000000000000000000000" + imm4_h + imm4_l
        t2 = rt.uint + 1
        if rt[3] or t2 == 15:
            print "unpredictable"
        else:
            return LdrdLiteralA1(instr, **{"add": add, "imm32": imm32, "t": rt.uint, "t2": t2})
