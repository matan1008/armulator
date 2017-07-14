from armulator.armv6.opcodes.abstract_opcodes.strd_register import StrdRegister
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.configurations import arch_version


class StrdRegisterA1(StrdRegister, Opcode):
    def __init__(self, instruction, add, wback, index, m, t, t2, n):
        Opcode.__init__(self, instruction)
        StrdRegister.__init__(self, add, wback, index, m, t, t2, n)

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
        t2 = rt.uint + 1
        wback = (not index) or w
        if rt[3] or (not index and w) or (t2 == 15 or rm.uint == 15) or (
                    wback and (rn.uint == 15 or rn.uint == rt.uint or rn.uint == t2)) or (
                            arch_version() < 6 and wback and rn.uint == rm.uint):
            print "unpredictable"
        else:
            return StrdRegisterA1(instr, **{"add": add, "wback": wback, "index": index, "m": rm.uint, "t": rt.uint,
                                            "t2": t2, "n": rn.uint})
