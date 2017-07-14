from armulator.armv6.opcodes.abstract_opcodes.msr_immediate_system import MsrImmediateSystem
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import arm_expand_imm


class MsrImmediateSystemA1(MsrImmediateSystem, Opcode):
    def __init__(self, instruction, write_spsr, mask, imm32):
        Opcode.__init__(self, instruction)
        MsrImmediateSystem.__init__(self, write_spsr, mask, imm32)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        mask = instr[12:16]
        imm12 = instr[20:32]
        write_spsr = instr[9]
        imm32 = arm_expand_imm(imm12)
        if mask == "0b0000":
            print "unpredictable"
        else:
            return MsrImmediateSystemA1(instr, **{"write_spsr": write_spsr, "mask": mask, "imm32": imm32})
