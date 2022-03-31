from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.ldrht import Ldrht


class LdrhtA1(Ldrht):
    @staticmethod
    def from_bitarray(instr, processor):
        imm4_l = substring(instr, 3, 0)
        imm4_h = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        post_index = True
        imm32 = chain(imm4_h, imm4_l, 4)
        if rt == 15 or rn == 15 or rt == rn:
            print('unpredictable')
        else:
            return LdrhtA1(instr, register_form=False, add=add, post_index=post_index, t=rt, n=rn, imm32=imm32)
