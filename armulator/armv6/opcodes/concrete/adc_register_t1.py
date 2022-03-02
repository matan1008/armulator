from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.adc_register import AdcRegister
from armulator.armv6.shift import SRType


class AdcRegisterT1(AdcRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        setflags = not processor.in_it_block()
        shift_t = SRType.LSL
        shift_n = 0
        return AdcRegisterT1(instr, setflags=setflags, m=rm, d=rdn, n=rdn, shift_t=shift_t, shift_n=shift_n)
