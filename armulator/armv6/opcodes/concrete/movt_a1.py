from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.abstract_opcodes.movt import Movt


class MovtA1(Movt):
    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = substring(instr, 11, 0)
        rd = substring(instr, 15, 12)
        imm4 = substring(instr, 19, 16)
        imm16 = chain(imm4, imm12, 12)
        if rd == 15:
            print('unpredictable')
        else:
            return MovtA1(instr, d=rd, imm16=imm16)
