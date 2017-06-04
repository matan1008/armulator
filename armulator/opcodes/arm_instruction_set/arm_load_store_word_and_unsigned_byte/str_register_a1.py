from armulator.opcodes.abstract_opcodes.str_register import StrRegister
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift
from armulator.configurations import arch_version


class StrRegisterA1(StrRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, n, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        StrRegister.__init__(self, add, wback, index, m, t, n, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rt = instr[16:20]
        rn = instr[12:16]
        index = instr[7]
        add = instr[8]
        w = instr[10]
        wback = (not index) and w
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        if rm.uint == 15 or (wback and (rn.uint == 15 or rn.uint == rt.uint)) or (
                            arch_version() < 6 and wback and rm.uint == rn.uint):
            print "unpredictable"
        else:
            return StrRegisterA1(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                           "n": rn.uint, "shift_t": shift_t, "shift_n": shift_n})
