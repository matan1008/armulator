from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrb_immediate_thumb import LdrbImmediateThumb


class LdrbImmediateThumbT1(LdrbImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        imm5 = substring(instr, 10, 6)
        index = True
        add = True
        wback = False
        return LdrbImmediateThumbT1(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm5)
