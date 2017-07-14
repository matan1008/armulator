from armulator.armv6.opcodes.abstract_opcodes.sub_register import SubRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class SubRegisterT2(SubRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        SubRegister.__init__(self, setflags, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_o = instr[26:28]
        imm2 = instr[24:26]
        rd = instr[20:24]
        imm3 = instr[17:20]
        rn = instr[12:16]
        setflags = instr[11]
        shift_t, shift_n = decode_imm_shift(type_o, imm3 + imm2)
        if rd.uint == 13 or (rd.uint == 15 and not setflags) or rn.uint == 15 or rm.uint in (13, 15):
            print "unpredictable"
        else:
            return SubRegisterT2(instr, **{"setflags": setflags, "m": rm.uint, "d": rd.uint, "n": rn.uint,
                                           "shift_t": shift_t, "shift_n": shift_n})
