from armulator.armv6.bits_ops import substring, set_bit_at
from armulator.armv6.opcodes.abstract_opcodes.pop_thumb import PopThumb


class PopThumbT3(PopThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rt = substring(instr, 15, 12)
        registers = set_bit_at(0, rt, 1)
        unaligned_allowed = True
        if rt == 13 or (rt == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return PopThumbT3(instr, registers=registers, unaligned_allowed=unaligned_allowed)
