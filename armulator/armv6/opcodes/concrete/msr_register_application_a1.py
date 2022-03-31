from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.msr_register_application import MsrRegisterApplication


class MsrRegisterApplicationA1(MsrRegisterApplication):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 3, 0)
        write_nzcvq = bit_at(instr, 19)
        write_g = bit_at(instr, 18)
        if rn == 15 or (not write_g and not write_nzcvq):
            print('unpredictable')
        else:
            return MsrRegisterApplicationA1(instr, write_nzcvq=write_nzcvq, write_g=write_g, n=rn)
