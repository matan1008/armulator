from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.srs_thumb import SrsThumb


class SrsThumbT1(SrsThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        mode = substring(instr, 4, 0)
        wback = bit_at(instr, 21)
        wordhigher = False
        return SrsThumbT1(instr, increment=False, word_higher=wordhigher, wback=wback, mode=mode)
