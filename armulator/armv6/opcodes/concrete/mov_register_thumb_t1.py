from armulator.armv6.bits_ops import substring, chain, bit_at
from armulator.armv6.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb


class MovRegisterThumbT1(MovRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = chain(bit_at(instr, 7), substring(instr, 2, 0), 3)
        rm = substring(instr, 6, 3)
        setflags = False
        if rd == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return MovRegisterThumbT1(instr, setflags=setflags, m=rm, d=rd)
