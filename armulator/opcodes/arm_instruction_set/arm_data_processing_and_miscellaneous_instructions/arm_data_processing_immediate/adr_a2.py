from armulator.opcodes.abstract_opcodes.adr import Adr
from armulator.opcodes.opcode import Opcode
from armulator.shift import arm_expand_imm


class AdrA2(Adr, Opcode):
    def __init__(self, instruction, d, imm32):
        Opcode.__init__(self, instruction)
        Adr.__init__(self, False, d, imm32)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        imm32 = arm_expand_imm(imm12)
        rd = instr[16:20]
        return AdrA2(instr, **{"d": rd.uint, "imm32": imm32})
