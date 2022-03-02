from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mls import Mls


class MlsT1(Mls):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        ra = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        if rd in (13, 15) or rn in (13, 15) or rm in (13, 15) or ra in (13, 15):
            print('unpredictable')
        else:
            return MlsT1(instr, m=rm, a=ra, d=rd, n=rn)
