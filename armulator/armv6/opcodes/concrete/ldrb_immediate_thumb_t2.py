from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrb_immediate_thumb import LdrbImmediateThumb


class LdrbImmediateThumbT2(LdrbImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = True
        add = True
        wback = False
        if rt == 13:
            print('unpredictable')
        else:
            return LdrbImmediateThumbT2(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
