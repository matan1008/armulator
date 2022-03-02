from armulator.armv6.bits_ops import substring, chain, bit_at, bit_count
from armulator.armv6.opcodes.abstract_opcodes.push import Push


class PushT2(Push):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 12, 0)
        m = bit_at(instr, 14)
        unaligned_allowed = True
        registers = chain(m, register_list, 14)
        if bit_count(registers, 1, 16) < 2:
            print('unpredictable')
        else:
            return PushT2(instr, registers=registers, unaligned_allowed=unaligned_allowed)
