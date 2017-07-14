from armulator.armv6.opcodes.abstract_opcodes.ldrht import Ldrht
from armulator.armv6.opcodes.opcode import Opcode


class LdrhtA2(Ldrht, Opcode):
    def __init__(self, instruction, add, post_index, t, n, m):
        Opcode.__init__(self, instruction)
        Ldrht.__init__(self, add, True, post_index, t, n, m=m)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rm = instr[-4:]
        rt = instr[16:20]
        rn = instr[12:16]
        add = instr[8]
        post_index = True
        if rt.uint == 15 or rn.uint == 15 or rt.uint == rn.uint or rm.uint == 15:
            print "unpredictable"
        else:
            return LdrhtA2(instr, **{"add": add, "post_index": post_index,
                                     "t": rt.uint, "n": rn.uint, "m": rm.uint})
