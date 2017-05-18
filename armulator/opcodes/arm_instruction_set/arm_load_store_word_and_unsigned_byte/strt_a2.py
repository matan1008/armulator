from armulator.opcodes.abstract_opcodes.strt import Strt
from armulator.opcodes.opcode import Opcode
from armulator.shift import decode_imm_shift
from armulator.configurations import ArchVersion


class StrtA2(Strt, Opcode):
    def __init__(self, instruction, add, post_index, t, n, m, shift_t, shift_n):
        Opcode.__init__(self, instruction)
        Strt.__init__(self, add, True, post_index, t, n, m, shift_t, shift_n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[28:32]
        type_o = instr[25:27]
        imm5 = instr[20:25]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        shift_t, shift_n = decode_imm_shift(type_o, imm5)
        post_index = True
        if rn.uint == 15 or rn.uint == rt.uint or rm.uint or (ArchVersion() < 6 and rm.uint == rn.uint):
            print "unpredictable"
        else:
            return StrtA2(instr, **{"add": add, "post_index": post_index, "t": rt.uint,
                                    "n": rn.uint, "m": rm.uint, "shift_t": shift_t, "shift_n": shift_n})
