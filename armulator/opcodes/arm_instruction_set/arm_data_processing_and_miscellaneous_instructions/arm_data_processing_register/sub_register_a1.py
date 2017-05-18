from armulator.opcodes.abstract_opcodes.sub_register import SubRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift


class SubRegisterA1(SubRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        SubRegister.__init__(self, setflags, m, d, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rd = instr[16:20]
        rn = instr[12:16]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return SubRegisterA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint, "n": rn.uint, "shift_t": shift_t,
                                       "shift_n": shift_n})
