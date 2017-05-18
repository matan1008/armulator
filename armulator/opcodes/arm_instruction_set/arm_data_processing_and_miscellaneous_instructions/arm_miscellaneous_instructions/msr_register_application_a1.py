from armulator.opcodes.abstract_opcodes.msr_register_application import MsrRegisterApplication
from armulator.opcodes.opcode import Opcode


class MsrRegisterApplicationA1(MsrRegisterApplication, Opcode):
    def __init__(self, instruction, write_nzcvq, write_g, n):
        Opcode.__init__(self, instruction)
        MsrRegisterApplication.__init__(self, write_nzcvq, write_g, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[-4:]
        write_nzcvq = instr[12]
        write_g = instr[13]
        if rn.uint == 15 or (not write_g and not write_nzcvq):
            print "unpredictable"
        else:
            return MsrRegisterApplicationA1(instr, **{"write_nzcvq": write_nzcvq, "write_g": write_g, "n": rn.uint})
