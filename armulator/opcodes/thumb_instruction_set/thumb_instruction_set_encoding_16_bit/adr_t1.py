from armulator.opcodes.abstract_opcodes.adr import Adr
from armulator.opcodes.opcode import Opcode
from armulator.bits_ops import zero_extend


class AdrT1(Adr, Opcode):
    def __init__(self, instruction, add, d, imm32):
        Opcode.__init__(self, instruction)
        Adr.__init__(self, add, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[8:16]
        rd = instr[5:8]
        add = True
        imm32 = zero_extend(imm8 + "0b00", 32)
        return AdrT1(instr, **{"add": add, "d": rd.uint, "imm32": imm32})
