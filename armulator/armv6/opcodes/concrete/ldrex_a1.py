from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrex import Ldrex


class LdrexA1(Ldrex):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        imm32 = 0
        if rn == 15 or rt == 15:
            print('unpredictable')
        else:
            return LdrexA1(instr, imm32=imm32, t=rt, n=rn)
