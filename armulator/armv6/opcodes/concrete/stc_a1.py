from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.stc_stc2 import StcStc2


class StcStc2A1(StcStc2):
    @staticmethod
    def from_bitarray(instr, processor):
        imm8 = substring(instr, 7, 0)
        coproc = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        wback = bit_at(instr, 21)
        add = bit_at(instr, 23)
        index = bit_at(instr, 24)
        d = bit_at(instr, 22)
        if not index and not add and not d and not wback:
            raise UndefinedInstructionException()
        elif rn == 15 and wback:
            print('unpredictable')
        else:
            imm32 = imm8 << 2
            return StcStc2A1(instr, cp=coproc, n=rn, add=add, imm32=imm32, index=index, wback=wback)
