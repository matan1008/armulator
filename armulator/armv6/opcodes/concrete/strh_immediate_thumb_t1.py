from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strh_immediate_thumb import StrhImmediateThumb


class StrhImmediateThumbT1(StrhImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        imm5 = substring(instr, 10, 6)
        index = True
        add = True
        wback = False
        imm32 = imm5 << 2
        return StrhImmediateThumbT1(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
