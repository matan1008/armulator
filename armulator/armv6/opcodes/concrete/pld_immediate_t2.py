from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pld_immediate import PldImmediate


class PldImmediateT2(PldImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        rn = substring(instr, 19, 16)
        is_pldw = bit_at(instr, 21)
        return PldImmediateT2(instr, add=False, is_pldw=is_pldw, n=rn, imm32=imm32)
