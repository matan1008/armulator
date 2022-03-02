from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strt import Strt


class StrtT1(Strt):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = True
        post_index = False
        if rn == 0b1111:
            raise UndefinedInstructionException()
        elif rt in (13, 15):
            print('unpredictable')
        else:
            return StrtT1(instr, register_form=False, add=add, post_index=post_index, t=rt, n=rn, imm32=imm32)
