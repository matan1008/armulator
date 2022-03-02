from armulator.armv6.bits_ops import sign_extend, substring
from armulator.armv6.opcodes.abstract_opcodes.b import B


class BA1(B):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = sign_extend(substring(instr, 23, 0) << 2, 26, 32)
        return BA1(instr, imm32=imm32)
