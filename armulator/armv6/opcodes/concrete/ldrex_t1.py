from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrex import Ldrex


class LdrexT1(Ldrex):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        imm32 = imm8 << 2
        if rt in (13, 15) or rn == 15:
            print('unpredictable')
        else:
            return LdrexT1(instr, imm32=imm32, t=rt, n=rn)
