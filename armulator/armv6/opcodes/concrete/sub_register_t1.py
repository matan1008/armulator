from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.sub_register import SubRegister
from armulator.armv6.shift import SRType


class SubRegisterT1(SubRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rn = substring(instr, 5, 3)
        rm = substring(instr, 8, 6)
        set_flags = not processor.in_it_block()
        shift_t = SRType.LSL
        shift_n = 0
        return SubRegisterT1(instr, setflags=set_flags, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
