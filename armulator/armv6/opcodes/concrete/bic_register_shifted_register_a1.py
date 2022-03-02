from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.bic_register_shifted_register import BicRegisterShiftedRegister
from armulator.armv6.shift import decode_reg_shift


class BicRegisterShiftedRegisterA1(BicRegisterShiftedRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        rs = substring(instr, 11, 8)
        rd = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        s = bit_at(instr, 20)
        if rd == 0b1111 or rn == 0b1111 or rm == 0b1111 or rs == 0b1111:
            print('unpredictable')
        else:
            shift_t = decode_reg_shift(type_o)
            return BicRegisterShiftedRegisterA1(instr, setflags=s, m=rm, s=rs, d=rd, n=rn, shift_t=shift_t)
