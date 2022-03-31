from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb


class MovRegisterThumbT2(MovRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rd = substring(instr, 2, 0)
        rm = substring(instr, 5, 3)
        if processor.in_it_block():
            print('unpredictable')
        else:
            return MovRegisterThumbT2(instr, m=rm, d=rd, setflags=True)
