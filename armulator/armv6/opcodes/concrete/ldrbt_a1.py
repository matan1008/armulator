from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrbt import Ldrbt


class LdrbtA1(Ldrbt):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        imm32 = substring(instr, 11, 0)
        add = bit_at(instr, 23)
        post_index = True
        if rt == 15 or rn == 15 or rt == rn:
            print('unpredictable')
        else:
            return LdrbtA1(instr, register_form=False, add=add, post_index=post_index, t=rt, n=rn, imm32=imm32)
