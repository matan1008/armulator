from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldr_immediate_thumb import LdrImmediateThumb


class LdrImmediateThumbT3(LdrImmediateThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        index = True
        add = True
        wback = False
        imm32 = substring(instr, 11, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rt == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return LdrImmediateThumbT3(instr, add=add, wback=wback, index=index, t=rt, n=rn, imm32=imm32)
