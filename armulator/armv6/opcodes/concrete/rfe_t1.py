from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.rfe import Rfe


class RfeT1(Rfe):
    @staticmethod
    def from_bitarray(instr, processor):
        rn = substring(instr, 19, 16)
        wback = bit_at(instr, 21)
        wordhigher = False
        if rn == 15 or (processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return RfeT1(instr, increment=False, word_higher=wordhigher, wback=wback, n=rn)
