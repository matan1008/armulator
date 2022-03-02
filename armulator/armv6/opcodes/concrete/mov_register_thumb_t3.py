from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.mov_register_thumb import MovRegisterThumb


class MovRegisterThumbT3(MovRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        rd = substring(instr, 11, 8)
        setflags = bit_at(instr, 20)
        if (setflags and (rd in (13, 15) or rm in (13, 15))) or \
                (not setflags and (rd == 15 or rm == 15 or (rd == 13 and rm == 13))):
            print('unpredictable')
        else:
            return MovRegisterThumbT3(instr, setflags=setflags, m=rm, d=rd)
