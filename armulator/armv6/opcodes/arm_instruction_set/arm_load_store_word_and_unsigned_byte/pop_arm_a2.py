from armulator.armv6.opcodes.abstract_opcodes.pop_arm import PopArm
from armulator.armv6.opcodes.opcode import Opcode
from bitstring import BitArray


class PopArmA2(PopArm, Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        Opcode.__init__(self, instruction)
        PopArm.__init__(self, registers, unaligned_allowed)

    def is_pc_changing_opcode(self):
        return False

    @staticmethod
    def from_bitarray(instr, processor):
        rt = instr[16:20]
        registers = BitArray(length=16)
        registers[15 - rt.uint] = True
        unaligned_allowed = True
        if rt.uint == 13:
            print("unpredictable")
        else:
            return PopArmA2(instr, **{"registers": registers, "unaligned_allowed": unaligned_allowed})
