from armulator.armv6.bits_ops import substring, chain
from armulator.armv6.opcodes.abstract_opcodes.tst_register import TstRegister
from armulator.armv6.shift import decode_imm_shift


class TstRegisterT2(TstRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 5, 4)
        imm2 = substring(instr, 7, 6)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        shift_t, shift_n = decode_imm_shift(type_o, chain(imm3, imm2, 2))
        if rn in (13, 15) or rm in (13, 15):
            print('unpredictable')
        else:
            return TstRegisterT2(instr, m=rm, n=rn, shift_t=shift_t, shift_n=shift_n)
