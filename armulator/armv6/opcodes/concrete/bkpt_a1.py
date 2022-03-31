from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.abstract_opcodes.bkpt import Bkpt


class BkptA1(Bkpt):
    @staticmethod
    def from_bitarray(instr, processor):
        imm4 = substring(instr, 3, 0)
        imm12 = substring(instr, 19, 8)
        imm32 = chain(imm12, imm4, 4)
        if substring(instr, 31, 28) != 0b1110:
            print('unpredictable')
        else:
            return BkptA1(instr)
