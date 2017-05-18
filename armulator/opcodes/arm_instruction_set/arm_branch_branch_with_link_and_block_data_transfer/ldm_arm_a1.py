from armulator.opcodes.abstract_opcodes.ldm_arm import LdmArm
from armulator.opcodes.opcode import Opcode
from armulator.configurations import ArchVersion


class LdmArmA1(LdmArm, Opcode):
    def __init__(self, instruction, wback, registers, n):
        Opcode.__init__(self, instruction)
        LdmArm.__init__(self, wback, registers, n)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        rn = instr[12:16]
        wback = instr[10]
        if rn.uint == 15 or register_list.count(1) < 1 or (
                        wback and register_list[15 - rn.uint] and ArchVersion() >= 7):
            print "unpredictable"
        else:
            return LdmArmA1(instr, **{"wback": wback, "registers": register_list, "n": rn.uint})
