from armulator.opcodes.abstract_opcodes.tst_register import TstRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class TstRegisterT1(TstRegister, Opcode):
    def __init__(self, instruction, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        TstRegister.__init__(self, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[13:16]
        rm = instr[10:13]
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return TstRegisterT1(instr, **{"m": rm.uint, "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
