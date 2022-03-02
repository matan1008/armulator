from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.bic_register import BicRegister
from armulator.armv6.shift import SRType


class BicRegisterT1(BicRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        shift_t = SRType.LSL
        shift_n = 0
        return BicRegisterT1(instr, setflags=setflags, m=rm, d=rdn, n=rdn, shift_t=shift_t, shift_n=shift_n)
