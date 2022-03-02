from armulator.armv6.bits_ops import substring, chain, bit_at
from armulator.armv6.opcodes.abstract_opcodes.orr_register import OrrRegister
from armulator.armv6.shift import decode_imm_shift


class OrrRegisterT2(OrrRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 5, 4)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        setflags = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(type_o, chain(imm3, imm2, 2))
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return OrrRegisterT2(instr, setflags=setflags, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
