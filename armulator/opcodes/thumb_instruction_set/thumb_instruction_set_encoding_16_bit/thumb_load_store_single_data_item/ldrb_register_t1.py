from armulator.opcodes.abstract_opcodes.ldrb_register import LdrbRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import SRType


class LdrbRegisterT1(LdrbRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrbRegister.__init__(self, add, wback, index, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[13:16]
        rn = instr[10:13]
        rm = instr[7:10]
        index = True
        add = True
        wback = False
        shift_t = SRType.SRType_LSL
        shift_n = 0
        return LdrbRegisterT1(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                        "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
