from armulator.opcodes.abstract_opcodes.pld_register import PldRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift


class PldRegisterA1(PldRegister, Opcode):
    def __init__(self, instruction, add, is_pldw, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        PldRegister.__init__(self, add, is_pldw, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rn = instr[12:16]
        is_pldw = instr[9]
        add = instr[8]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        if rm.uint == 15 or (rn.uint == 15 and is_pldw):
            print "unpredictable"
        else:
            return PldRegisterA1(instr, **{"add": add, "is_pldw": is_pldw, "m": rm.uint, "n": rn.uint,
                                           "shift_t": shift_t, "shift_n": shift_n})
