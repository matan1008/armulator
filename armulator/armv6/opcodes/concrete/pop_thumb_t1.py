from armulator.armv6.bits_ops import substring, bit_at, chain
from armulator.armv6.opcodes.abstract_opcodes.pop_thumb import PopThumb


class PopThumbT1(PopThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        unaligned_allowed = False
        registers_list = substring(instr, 7, 0)
        p = bit_at(instr, 8)
        registers = chain(p, registers_list, 15)
        if not registers or (bit_at(registers, 15) and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return PopThumbT1(instr, registers=registers, unaligned_allowed=unaligned_allowed)
