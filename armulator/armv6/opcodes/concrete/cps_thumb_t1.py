from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.abstract_opcodes.cps_thumb import CpsThumb


class CpsThumbT1(CpsThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        affect_a = bit_at(instr, 2)
        affect_i = bit_at(instr, 1)
        affect_f = bit_at(instr, 0)
        enable = not bit_at(instr, 4)
        disable = bit_at(instr, 4)
        if (not affect_a and not affect_i and not affect_f) or processor.in_it_block():
            print('unpredictable')
        else:
            return CpsThumbT1(instr, affect_a=affect_a, affect_i=affect_i, affect_f=affect_f, enable=enable,
                              disable=disable, change_mode=False)
