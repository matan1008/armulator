from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.strh_immediate_thumb import StrhImmediateThumb


class StrhImmediateThumbT3(StrhImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        wback = bit_at(instr, 8)
        add = bit_at(instr, 9)
        index = bit_at(instr, 10)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rn == 0b1111 or (not index and not wback):
            raise UndefinedInstructionException()
        elif rt in (13, 15) or (wback and rn == rt):
            print('unpredictable')
        else:
            return StrhImmediateThumbT3(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
