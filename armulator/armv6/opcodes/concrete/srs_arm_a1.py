from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.srs_arm import SrsArm


class SrsArmA1(SrsArm):
    @staticmethod
    def from_bitarray(instr, processor):
        mode = substring(instr, 4, 0)
        wback = bit_at(instr, 21)
        increment = bit_at(instr, 23)
        p = bit_at(instr, 24)
        word_higher = p == increment
        return SrsArmA1(instr, increment=increment, word_higher=word_higher, wback=wback, mode=mode)
