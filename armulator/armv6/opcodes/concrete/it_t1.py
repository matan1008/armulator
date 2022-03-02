from armulator.armv6.bits_ops import substring, bit_count
from armulator.armv6.opcodes.abstract_opcodes.it import It


class ItT1(It):
    @staticmethod
    def from_bitarray(instr, processor):
        mask = substring(instr, 3, 0)
        first_cond = substring(instr, 7, 4)
        if first_cond == 0b1111 or (first_cond == 0b1110 and bit_count(mask, 1, 4) != 1) or processor.in_it_block():
            print('unpredictable')
        else:
            return ItT1(instr, firstcond=first_cond, mask=mask)
