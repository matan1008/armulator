from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.movt import Movt


class MovtT1(Movt):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        imm4 = substring(instr, 19, 16)
        i = bit_at(instr, 26)
        imm16 = chain(imm4, chain(i, chain(imm3, imm8, 8), 11), 12)
        if rd in (13, 15):
            print('unpredictable')
        else:
            return MovtT1(instr, d=rd, imm16=imm16)
