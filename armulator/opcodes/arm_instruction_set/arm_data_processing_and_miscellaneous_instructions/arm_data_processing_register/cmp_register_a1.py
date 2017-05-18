from armulator.opcodes.abstract_opcodes.cmp_register import CmpRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift


class CmpRegisterA1(CmpRegister, Opcode):
    def __init__(self, instruction, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        CmpRegister.__init__(self, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rn = instr[12:16]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        return CmpRegisterA1(instr, **{"m": rm.uint, "n": rn.uint, "shift_t": shift_t,
                                       "shift_n": shift_n})
