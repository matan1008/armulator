from armulator.opcodes.abstract_opcodes.cmn_register import CmnRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class CmnRegisterT1(CmnRegister, Opcode):
    def __init__(self, instruction, m, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        CmnRegister.__init__(self, m, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[13:16]
        rm = instr[10:13]
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return CmnRegisterT1(instr, **{"m": rm.uint, "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
