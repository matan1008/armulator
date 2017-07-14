from armulator.armv6.opcodes.abstract_opcodes.msr_immediate_application import MsrImmediateApplication
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import arm_expand_imm


class MsrImmediateApplicationA1(MsrImmediateApplication, Opcode):
    def __init__(self, instruction, write_nzcvq, write_g, imm32):
        Opcode.__init__(self, instruction)
        MsrImmediateApplication.__init__(self, write_nzcvq, write_g, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        imm12 = instr[20:32]
        imm32 = arm_expand_imm(imm12)
        mask = instr[12:14]
        write_nzcvq = mask[0]
        write_g = mask[1]
        return MsrImmediateApplicationA1(instr, **{"write_nzcvq": write_nzcvq, "write_g": write_g, "imm32": imm32})
