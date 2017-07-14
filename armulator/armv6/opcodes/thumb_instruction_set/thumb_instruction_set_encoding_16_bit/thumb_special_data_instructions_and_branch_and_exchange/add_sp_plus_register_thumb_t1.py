from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class AddSpPlusRegisterThumbT1(AddSpPlusRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        AddSpPlusRegisterThumb.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rdm = instr[8:9] + instr[13:16]
        setflags = False
        shift_t = SRType.SRType_LSL
        shift_n = 0
        if rdm.uint == 15 and processor.in_it_block() and not processor.last_in_it_block():
            print "unpredictable"
        else:
            return AddSpPlusRegisterThumbT1(instr, **{"setflags": setflags, "m": rdm.uint, "d": rdm.uint,
                                                      "shift_t": shift_t, "shift_n": shift_n})
