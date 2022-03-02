from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.armv6.shift import decode_imm_shift, SRType


class AddSpPlusRegisterThumbT3(AddSpPlusRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_ = substring(instr, 5, 4)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        setflags = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(type_, chain(imm3, imm2, 2))
        if rd == 13 and (shift_t != SRType.LSL or shift_n > 3) or (rd == 15 and not setflags) or rm in (13, 15):
            print('unpredictable')
        else:
            return AddSpPlusRegisterThumbT3(instr, setflags=setflags, m=rm, d=rd, shift_t=shift_t, shift_n=shift_n)
