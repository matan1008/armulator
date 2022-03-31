from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.tbb_tbh import TbbTbh


class TbbTbhT1(TbbTbh):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        is_tbh = bit_at(instr, 4)
        rn = substring(instr, 19, 16)
        if rn == 13 or rm in (13, 15) or (processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return TbbTbhT1(instr, is_tbh=is_tbh, m=rm, n=rn)
