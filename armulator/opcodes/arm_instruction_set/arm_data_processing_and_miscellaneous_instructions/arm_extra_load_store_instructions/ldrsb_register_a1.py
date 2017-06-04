from armulator.opcodes.abstract_opcodes.ldrsb_register import LdrsbRegister
from armulator.opcodes.opcode import Opcode
from armulator.configurations import arch_version
from armulator.shift import SRType


class LdrsbRegisterA1(LdrsbRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrsbRegister.__init__(self, add, wback, index, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        w = instr[10]
        index = instr[7]
        wback = (not index) or w
        shift_t = SRType.SRType_LSL
        shift_n = 0
        if rt.uint == 15 or rm.uint == 15 or (wback and (rn.uint == 15 and rn.uint == rt.uint)) or (
                            arch_version() < 6 and wback and rm.uint == rn.uint):
            print "unpredictable"
        else:
            return LdrsbRegisterA1(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                             "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
