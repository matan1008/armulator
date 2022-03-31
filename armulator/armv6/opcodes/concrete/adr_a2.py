from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.adr import Adr
from armulator.armv6.shift import arm_expand_imm


class AdrA2(Adr):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        imm32 = arm_expand_imm(imm12)
        rd = substring(instr, 15, 12)
        return AdrA2(instr, add=False, d=rd, imm32=imm32)
