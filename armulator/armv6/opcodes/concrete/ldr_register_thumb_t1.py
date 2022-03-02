from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldr_register_thumb import LdrRegisterThumb
from armulator.armv6.shift import SRType


class LdrRegisterThumbT1(LdrRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        rm = substring(instr, 8, 6)
        shift_t = SRType.LSL
        shift_n = 0
        return LdrRegisterThumbT1(instr, m=rm, t=rt, n=rn, shift_t=shift_t, shift_n=shift_n)
