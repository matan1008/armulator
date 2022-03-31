from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.cps_arm import CpsArm


class CpsArmA1(CpsArm):
    @staticmethod
    def from_bitarray(instr, processor):
        mode = substring(instr, 4, 0)
        f = bit_at(instr, 6)
        i = bit_at(instr, 7)
        a = bit_at(instr, 8)
        m = bit_at(instr, 17)
        imod = substring(instr, 19, 18)
        if (mode != 0b00000 and not m) or (
                (bit_at(imod, 1) and not (a or f or i)) or (not bit_at(imod, 1) and (a or f or i))) or (
                (imod == 0b00 and not m) or imod == 0b01):
            print('unpredictable')
        else:
            enable = imod == 0b10
            disable = imod == 0b11
            return CpsArmA1(instr, affect_a=a, affect_i=i, affect_f=f, enable=enable, disable=disable, change_mode=m,
                            mode=mode)
