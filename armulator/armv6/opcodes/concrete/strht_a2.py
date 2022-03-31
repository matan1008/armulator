from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.strht import Strht


class StrhtA2(Strht):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        post_index = True
        if rt == 15 or rn == 15 or rt == rn or rm == 15:
            print('unpredictable')
        else:
            return StrhtA2(instr, register_form=True, add=add, post_index=post_index, t=rt, n=rn, m=rm)
