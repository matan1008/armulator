from armulator.armv6.bits_ops import chain, substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.armv6.shift import SRType


class AddSpPlusRegisterThumbT1(AddSpPlusRegisterThumb):
    @staticmethod
    def from_bitarray(instr, processor):
        rdm = chain(bit_at(instr, 7), substring(instr, 2, 0), 3)
        setflags = False
        shift_t = SRType.LSL
        shift_n = 0
        if rdm == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print('unpredictable')
        else:
            return AddSpPlusRegisterThumbT1(instr, setflags=setflags, m=rdm, d=rdm, shift_t=shift_t, shift_n=shift_n)
