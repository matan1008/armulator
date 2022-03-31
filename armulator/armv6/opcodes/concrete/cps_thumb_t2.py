from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.cps_thumb import CpsThumb


class CpsThumbT2(CpsThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        mode = substring(instr, 4, 0)
        affect_f = bit_at(instr, 5)
        affect_i = bit_at(instr, 6)
        affect_a = bit_at(instr, 7)
        change_mode = bit_at(instr, 8)
        imod = substring(instr, 10, 9)
        imod_1 = bit_at(imod, 1)
        enable = imod == 0b10
        disable = imod == 0b11
        if (mode != 0b00000 and not change_mode) or (
                imod_1 and not affect_a and not affect_f and not affect_i) or (
                not imod_1 and (affect_a or affect_i or affect_f)) or imod == 0b01 or processor.in_it_block():
            print('unpredictable')
        else:
            return CpsThumbT2(instr, affect_a=affect_a, affect_i=affect_i, affect_f=affect_f, enable=enable,
                              disable=disable, change_mode=change_mode, mode=mode)
