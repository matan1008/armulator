from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mrrc_mrrc2 import MrrcMrrc2


class MrrcMrrc2A1(MrrcMrrc2):
    @staticmethod
    def from_bitarray(instr, processor):
        coproc = substring(instr, 11, 8)
        rt = substring(instr, 15, 12)
        rt2 = substring(instr, 19, 16)
        if rt == 15 or rt2 == 15 or rt == rt2:
            print('unpredictable')
        else:
            return MrrcMrrc2A1(instr, cp=coproc, t=rt, t2=rt2)
