from armulator.armv6.bits_ops import substring, set_bit_at
from armulator.armv6.opcodes.abstract_opcodes.push import Push


class PushA2(Push):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        registers = set_bit_at(0, rt, 1)
        unaligned_allowed = True
        if rt == 13:
            print('unpredictable')
        else:
            return PushA2(instr, registers=registers, unaligned_allowed=unaligned_allowed)
