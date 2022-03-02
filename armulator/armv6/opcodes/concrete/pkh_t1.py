from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.pkh import Pkh
from armulator.armv6.shift import decode_imm_shift


class PkhT1(Pkh):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        tbform = bit_at(instr, 5)
        t = bit_at(instr, 4)
        imm2 = substring(instr, 7, 6)
        rd = substring(instr, 11, 8)
        imm3 = substring(instr, 14, 12)
        rn = substring(instr, 19, 16)
        s = bit_at(instr, 20)
        shift_t, shift_n = decode_imm_shift(tbform << 1, chain(imm3, imm2, 2))
        if s or t:
            raise UndefinedInstructionException()
        elif rn in (13, 15) or rm in (13, 15) or rd in (13, 15):
            print('unpredictable')
        else:
            return PkhT1(instr, tb_form=tbform, m=rm, d=rd, n=rn, shift_t=shift_t, shift_n=shift_n)
