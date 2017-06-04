from armulator.opcodes.abstract_opcodes.pop_arm import PopArm
from armulator.opcodes.opcode import Opcode
from armulator.configurations import arch_version


class PopArmA1(PopArm, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        PopArm.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return self.registers[0]

    @staticmethod
    def from_bitarray(instr, processor):
        register_list = instr[16:32]
        unaligned_allowed = False
        if register_list[2] and arch_version() >= 7:
            print "unpredictable"
        else:
            return PopArmA1(instr, **{"registers": register_list, "unaligned_allowed": unaligned_allowed})
