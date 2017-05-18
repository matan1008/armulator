from armulator.opcodes.abstract_opcodes.ldrsh_register import LdrshRegister
from armulator.opcodes.opcode import Opcode
from armulator.configurations import ArchVersion
from armulator.shift import SRType


class LdrshRegisterA1(LdrshRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        LdrshRegister.__init__(self, add, wback, index, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        w = instr[10]
        index = instr[7]
        rm = instr[-4:]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        wback = (not index) or w
        shift_t = SRType.SRType_LSL
        shift_n = 0
        if rt.uint == 15 or rm.uint == 15 or (wback and (rn.uint == 15 or rn.uint == rt.uint)) or (
                            ArchVersion() < 6 and wback and rm.uint == rn.uint):
            print "unpredictable"
        else:
            return LdrshRegisterA1(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                             "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
