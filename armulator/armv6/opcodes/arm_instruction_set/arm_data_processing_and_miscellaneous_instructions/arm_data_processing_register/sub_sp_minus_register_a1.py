from armulator.armv6.opcodes.abstract_opcodes.sub_sp_minus_register import SubSpMinusRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import decode_imm_shift


class SubSpMinusRegisterA1(SubSpMinusRegister, Opcode):
    def __init__(self, instruction, setflags, m, d, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        SubSpMinusRegister.__init__(self, setflags, m, d, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return self.d == 15

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rd = instr[16:20]
        s = instr[11]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return SubSpMinusRegisterA1(instr, **{"setflags": s, "m": rm.uint, "d": rd.uint, "shift_t": shift_t,
                                              "shift_n": shift_n})
