from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldr_register_thumb import LdrRegisterThumb
from armulator.armv6.shift import SRType


class LdrRegisterThumbT2(LdrRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        imm2 = substring(instr, 5, 4)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rm in (13, 15) or (rt == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return LdrRegisterThumbT2(instr, m=rm, t=rt, n=rn, shift_t=SRType.LSL, shift_n=imm2)
