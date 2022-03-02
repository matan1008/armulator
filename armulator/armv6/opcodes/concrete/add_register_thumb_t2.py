from armulator.armv6.bits_ops import bit_at, chain, substring
from armulator.armv6.opcodes.abstract_opcodes.add_register_thumb import AddRegisterThumb
from armulator.armv6.shift import SRType


class AddRegisterThumbT2(AddRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rdn = chain(bit_at(instr, 7), substring(instr, 2, 0), 3)
        rm = substring(instr, 6, 3)
        setflags = False
        shift_t = SRType.LSL
        shift_n = 0
        if (rdn == 15 and rm == 15) or (rdn == 15 and processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return AddRegisterThumbT2(instr, setflags=setflags, m=rm, d=rdn, n=rdn, shift_t=shift_t, shift_n=shift_n)
