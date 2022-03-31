from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldrb_immediate_thumb import LdrbImmediateThumb


class LdrbImmediateThumbT3(LdrbImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        rn = substring(instr, 19, 16)
        rt = substring(instr, 15, 12)
        index = bit_at(instr, 10)
        add = bit_at(instr, 9)
        wback = bit_at(instr, 8)
        if not index and not wback:
            raise UndefinedInstructionException()
        elif rt == 13 or (rt == 15 and wback) or (wback and rn == rt):
            print('unpredictable')
        else:
            return LdrbImmediateThumbT3(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
