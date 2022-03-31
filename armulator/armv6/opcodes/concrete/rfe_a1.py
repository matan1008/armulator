from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.opcodes.abstract_opcodes.rfe import Rfe


class RfeA1(Rfe):
    @staticmethod
    def from_bitarray(instr, processor):
        wback = bit_at(instr, 21)
        increment = bit_at(instr, 23)
        p = bit_at(instr, 24)
        word_higher = p == increment
        rn = substring(instr, 19, 16)
        if rn == 15:
            print('unpredictable')
        else:
            return RfeA1(instr, increment=increment, word_higher=word_higher, wback=wback, n=rn)
