from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.strt import Strt


class StrtA1(Strt):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        post_index = True
        if rn == 15 or rn == rt:
            print('unpredictable')
        else:
            return StrtA1(instr, register_form=False, add=add, post_index=post_index, t=rt, n=rn, imm32=imm32)
