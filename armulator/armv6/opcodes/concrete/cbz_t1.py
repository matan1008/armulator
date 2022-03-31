from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.cbz import Cbz


class CbzT1(Cbz):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 2, 0)
        imm5 = substring(instr, 7, 3)
        i = bit_at(instr, 9)
        nonzero = bit_at(instr, 11)
        imm32 = chain(i, imm5, 5) << 2
        return CbzT1(instr, nonzero=nonzero, n=rn, imm32=imm32)
