from armulator.armv6.bits_ops import substring, bit_at, set_bit_at
from armulator.armv6.opcodes.abstract_opcodes.push import Push


class PushT1(Push):
    @staticmethod
    def from_bitarray(instr, processor):
        registers_list = substring(instr, 7, 0)
        m = bit_at(instr, 8)
        registers = set_bit_at(registers_list, 14, m)
        unaligned_allowed = False
        if not registers:
            print('unpredictable')
        else:
            return PushT1(instr, registers=registers, unaligned_allowed=unaligned_allowed)
