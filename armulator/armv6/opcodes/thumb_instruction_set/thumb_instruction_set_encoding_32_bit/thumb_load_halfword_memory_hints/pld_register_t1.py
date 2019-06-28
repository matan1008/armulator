from armulator.armv6.opcodes.abstract_opcodes.pld_register import PldRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class PldRegisterT1(PldRegister, Opcode):
    def __init__(self, instruction, add, is_pldw, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        PldRegister.__init__(self, add, is_pldw, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        imm2 = instr[26:28]
        add = True
        is_pldw = instr[10]
        rn = instr[12:16]
        if rm.uint in (13, 15):
            print("unpredictable")
        else:
            return PldRegisterT1(instr, **{"add": add, "is_pldw": is_pldw, "m": rm.uint, "n": rn.uint,
                                           "shift_t": SRType.SRType_LSL, "shift_n": imm2.uint})
