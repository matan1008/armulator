from armulator.armv6.opcodes.abstract_opcodes.adr import Adr
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.bits_ops import zero_extend


class AdrT2(Adr, Opcode):
    def __init__(self, instruction, d, imm32):
        Opcode.__init__(self, instruction)
        Adr.__init__(self, False, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = instr[24:32]
        rd = instr[20:24]
        imm3 = instr[17:20]
        i = instr[5:6]
        imm32 = zero_extend(i + imm3 + imm8, 32)
        if rd.uint in (13, 15):
            print "unpredictable"
        else:
            return AdrT2(instr, **{"d": rd.uint, "imm32": imm32})
