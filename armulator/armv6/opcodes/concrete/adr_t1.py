from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.adr import Adr


class AdrT1(Adr):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 10, 8)
        add = True
        imm32 = imm8 << 2
        return AdrT1(instr, add=add, d=rd, imm32=imm32)
