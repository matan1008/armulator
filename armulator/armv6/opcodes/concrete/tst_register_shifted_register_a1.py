from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.tst_register_shifted_register import TstRegisterShiftedRegister
from armulator.armv6.shift import decode_reg_shift


class TstRegisterShiftedRegisterA1(TstRegisterShiftedRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        type_o = substring(instr, 6, 5)
        rs = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        if rn == 0b1111 or rm == 0b1111 or rs == 0b1111:
            print('unpredictable')
        else:
            shift_t = decode_reg_shift(type_o)
            return TstRegisterShiftedRegisterA1(instr, m=rm, s=rs, n=rn, shift_t=shift_t)
