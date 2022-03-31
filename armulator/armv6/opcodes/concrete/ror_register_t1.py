from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ror_register import RorRegister


class RorRegisterT1(RorRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        return RorRegisterT1(instr, setflags=setflags, m=rm, d=rdn, n=rdn)
