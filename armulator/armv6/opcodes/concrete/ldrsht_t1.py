from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrsht import Ldrsht


class LdrshtT1(Ldrsht):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        post_index = False
        add = True
        if rt in (13, 15):
            print('unpredictable')
        else:
            return LdrshtT1(instr, register_form=False, add=add, post_index=post_index, t=rt, n=rn, imm32=imm32)
