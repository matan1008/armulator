from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.ldr_immediate_thumb import LdrImmediateThumb


class LdrImmediateThumbT4(LdrImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        imm32 = substring(instr, 7, 0)
        wback = bit_at(instr, 8)
        add = bit_at(instr, 9)
        index = bit_at(instr, 10)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if not index and not wback:
            raise UndefinedInstructionException()
        elif (wback and rn == rt) or (rt == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return LdrImmediateThumbT4(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
