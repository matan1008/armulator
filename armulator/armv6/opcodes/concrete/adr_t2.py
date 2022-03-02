from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.adr import Adr


class AdrT2(Adr):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        i = bit_at(instr, 26)
        imm32 = chain(i, chain(imm3, imm8, 8), 11)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return AdrT2(instr, add=False, d=rd, imm32=imm32)
