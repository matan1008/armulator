from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.ldrsh_immediate import LdrshImmediate


class LdrshImmediateT2(LdrshImmediate):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = bit_at(instr, 10)
        add = bit_at(instr, 9)
        wback = bit_at(instr, 8)
        if not index and not wback:
            raise UndefinedInstructionException()
        elif rt == 13 or (rt == 15 and wback) or (wback and rt == rn):
            print('unpredictable')
        else:
            return LdrshImmediateT2(instr, add=add, wback=wback, index=index, imm32=imm32, t=rt, n=rn)
