from armulator.opcodes.abstract_opcodes.cmp_register import CmpRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class CmpRegisterT2(CmpRegister, Opcode):
    def __init__(self, instruction, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        CmpRegister.__init__(self, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[8:9] + instr[13:16]
        rm = instr[9:13]
        shift_t = SRType.SRType_LSL
        shift_n = 0
        if (rn.uint < 8 and rm.uint < 8) or rn.uint == 15 or rm.uint == 15:
            print "unpredictable"
        else:
            return CmpRegisterT2(instr, **{"m": rm.uint, "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
