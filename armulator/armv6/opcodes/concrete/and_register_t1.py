from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.and_register import AndRegister
from armulator.armv6.shift import SRType


class AndRegisterT1(AndRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        shift_t = SRType.LSL
        shift_n = 0
        return AndRegisterT1(instr, setflags=setflags, m=rm, d=rdn, n=rdn, shift_t=shift_t, shift_n=shift_n)
