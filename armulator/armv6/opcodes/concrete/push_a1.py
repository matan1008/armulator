from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.push import Push


class PushA1(Push):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 15, 0)
        unaligned_allowed = False
        return PushA1(instr, registers=register_list, unaligned_allowed=unaligned_allowed)
