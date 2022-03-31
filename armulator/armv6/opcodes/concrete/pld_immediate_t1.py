from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pld_immediate import PldImmediate


class PldImmediateT1(PldImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rn = substring(instr, 19, 16)
        is_pldw = bit_at(instr, 21)
        return PldImmediateT1(instr, add=True, is_pldw=is_pldw, n=rn, imm32=imm32)
