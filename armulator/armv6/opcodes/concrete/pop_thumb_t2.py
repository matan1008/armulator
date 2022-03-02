from armulator.armv6.bits_ops import substring, bit_count, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.pop_thumb import PopThumb


class PopThumbT2(PopThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 12, 0)
        p_m = substring(instr, 15, 14)
        registers = chain(p_m, register_list, 14)
        unaligned_allowed = False
        if bit_count(registers, 1, 16) < 2 or (p_m == 0b11) or (
                bit_at(registers, 15) and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return PopThumbT2(instr, registers=registers, unaligned_allowed=unaligned_allowed)
