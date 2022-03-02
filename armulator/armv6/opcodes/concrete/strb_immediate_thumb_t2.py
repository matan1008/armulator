from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.strb_immediate_thumb import StrbImmediateThumb


class StrbImmediateThumbT2(StrbImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = True
        add = True
        wback = False
        if rn == 0b1111:
            raise UndefinedInstructionException()
        elif rt in (13, 15):
            print('unpredictable')
        else:
            return StrbImmediateThumbT2(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
