from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.armv6.shift import SRType


class AddSpPlusRegisterThumbT2(AddSpPlusRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 6, 3)
        setflags = False
        shift_t = SRType.LSL
        shift_n = 0
        return AddSpPlusRegisterThumbT2(instr, setflags=setflags, m=rm, d=13, shift_t=shift_t, shift_n=shift_n)
