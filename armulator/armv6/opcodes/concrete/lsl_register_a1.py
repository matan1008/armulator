from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.lsl_register import LslRegister


class LslRegisterA1(LslRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        rm = substring(instr, 11, 8)
        rd = substring(instr, 15, 12)
        s = bit_at(instr, 20)
        if rd == 0b1111 or rn == 0b1111 or rm == 0b1111:
            print('unpredictable')
        else:
            return LslRegisterA1(instr, setflags=s, m=rm, d=rd, n=rn)
