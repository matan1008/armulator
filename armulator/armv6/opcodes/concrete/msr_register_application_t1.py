from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.msr_register_application import MsrRegisterApplication


class MsrRegisterApplicationT1(MsrRegisterApplication):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 19, 16)
        write_nzcvq = bit_at(instr, 11)
        write_g = bit_at(instr, 10)
        if (not write_g and not write_nzcvq) or rn in (13, 15):
            print('unpredictable')
        else:
            return MsrRegisterApplicationT1(instr, write_nzcvq=write_nzcvq, write_g=write_g, n=rn)
