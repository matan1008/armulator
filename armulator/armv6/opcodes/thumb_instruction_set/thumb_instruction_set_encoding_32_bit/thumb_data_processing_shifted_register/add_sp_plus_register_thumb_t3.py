from armulator.armv6.opcodes.abstract_opcodes.add_sp_plus_register_thumb import AddSpPlusRegisterThumb
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift, SRType


class AddSpPlusRegisterThumbT3(AddSpPlusRegisterThumb, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        AddSpPlusRegisterThumb.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_ = instr[26:28]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        setflags = instr[11]
        shift_t, shift_n = decode_imm_shift(type_, imm3 + imm2)
        if rd.uint == 13 and (shift_t != SRType.SRType_LSL or shift_n > 3) or (
                        rd.uint == 15 and not setflags) or rm.uint in (13, 15):
            print("unpredictable")
        else:
            return AddSpPlusRegisterThumbT3(instr, **{"setflags": setflags, "m": rm.uint,
                                                      "d": rd.uint, "shift_t": shift_t, "shift_n": shift_n})
