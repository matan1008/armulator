from armulator.armv6.opcodes.abstract_opcodes.ldrd_literal import LdrdLiteral
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class LdrdLiteralT1(LdrdLiteral, Opcode):
    def __init__(self, instruction, add, imm32, t, t2):
        Opcode.__init__(self, instruction)
        LdrdLiteral.__init__(self, add, imm32, t, t2)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rt2 = instr[20:24]
        rt = instr[16:20]
        add = instr[8]
        imm32 = zero_extend(imm8 + "0b00", 32)
        if rt.uint == rt2.uint or rt.uint in (13, 15) or rt2.uint in (13, 15) or instr[10]:
            print("unpredictable")
        else:
            return LdrdLiteralT1(instr, **{"add": add, "imm32": imm32, "t": rt.uint, "t2": rt2.uint})
