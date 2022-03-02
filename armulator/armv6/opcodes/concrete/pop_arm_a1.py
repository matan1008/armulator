from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.pop_arm import PopArm


class PopArmA1(PopArm):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 15, 0)
        unaligned_allowed = False
        if bit_at(register_list, 13) and arch_version() >= 7:
            print('unpredictable')
        else:
            return PopArmA1(instr, registers=register_list, unaligned_allowed=unaligned_allowed)
