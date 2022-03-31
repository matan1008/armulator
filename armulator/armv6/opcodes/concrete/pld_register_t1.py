from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.pld_register import PldRegister
from armulator.armv6.shift import SRType


class PldRegisterT1(PldRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        imm2 = substring(instr, 5, 4)
        rn = substring(instr, 19, 16)
        is_pldw = bit_at(instr, 21)
        add = True
        if rm in (13, 15):
            print('unpredictable')
        else:
            return PldRegisterT1(instr, add=add, is_pldw=is_pldw, m=rm, n=rn, shift_t=SRType.LSL, shift_n=imm2)
