from armulator.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class AddSpPlusRegisterThumbT2(AddSpPlusRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        AddSpPlusRegisterThumb.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[9:13]
        setflags = False
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return AddSpPlusRegisterThumbT2(instr, **{"setflags": setflags, "m": rm.uint, "d": 13,
                                                  "shift_t": shift_t, "shift_n": shift_n})
