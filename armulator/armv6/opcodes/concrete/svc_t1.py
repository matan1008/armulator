from armulator.armv6.bits_ops import to_unsigned, substring
from armulator.armv6.opcodes.abstract_opcodes.svc import Svc


class SvcT1(Svc):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        imm32 = to_unsigned(imm8, 32)
        return SvcT1(instr, imm32=imm32)
