from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.str_immediate_thumb import StrImmediateThumb


class StrImmediateThumbT2(StrImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        rt = substring(instr, 10, 8)
        index = True
        add = True
        wback = False
        imm32 = imm8 << 2
        return StrImmediateThumbT2(instr, add=add, wback=wback, index=index, t=rt, n=13, imm32=imm32)
