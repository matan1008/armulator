from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mvn_register import MvnRegister
from armulator.armv6.shift import SRType


class MvnRegisterT1(MvnRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        shift_t = SRType.LSL
        shift_n = 0
        return MvnRegisterT1(instr, setflags=setflags, m=rm, d=rd, shift_t=shift_t, shift_n=shift_n)
