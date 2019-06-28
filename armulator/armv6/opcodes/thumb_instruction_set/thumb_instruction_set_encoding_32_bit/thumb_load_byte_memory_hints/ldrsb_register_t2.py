from armulator.armv6.opcodes.abstract_opcodes.ldrsb_register import LdrsbRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import SRType


class LdrsbRegisterT2(LdrsbRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrsbRegister.__init__(self, add, wback, index, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        imm2 = instr[26:28]
        rt = instr[16:20]
        rn = instr[12:16]
        index = True
        add = True
        wback = False
        if rt.uint == 13 or rm.uint in (13, 15):
            print("unpredictable")
        else:
            return LdrsbRegisterT2(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                             "n": rn.uint, "shift_t": SRType.SRType_LSL, "shift_n": imm2.uint})
