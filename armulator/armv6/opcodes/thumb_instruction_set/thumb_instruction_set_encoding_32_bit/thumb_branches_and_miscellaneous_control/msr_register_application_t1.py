from armulator.armv6.opcodes.abstract_opcodes.msr_register_application import MsrRegisterApplication
from armulator.armv6.opcodes.opcode import Opcode


class MsrRegisterApplicationT1(MsrRegisterApplication, Opcode):
    def __init__(self, instruction, write_nzcvq, write_g, n):
        Opcode.__init__(self, instruction)
        MsrRegisterApplication.__init__(self, write_nzcvq, write_g, n)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rn = instr[12:16]
        write_nzcvq = instr[20]
        write_g = instr[21]
        if (not write_g and not write_nzcvq) or rn.uint in (13, 15):
            print("unpredictable")
        else:
            return MsrRegisterApplicationT1(instr, **{"write_nzcvq": write_nzcvq, "write_g": write_g, "n": rn.uint})
