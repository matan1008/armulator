from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrh_immediate_thumb import LdrhImmediateThumb


class LdrhImmediateThumbT1(LdrhImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        imm5 = substring(instr, 10, 6)
        index = True
        add = True
        wback = False
        imm32 = imm5 << 1
        return LdrhImmediateThumbT1(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
