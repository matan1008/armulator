from armulator.armv6.bits_ops import bit_at
from armulator.armv6.opcodes.abstract_opcodes.enterx_leavex import EnterxLeavex


class EnterxLeavexT1(EnterxLeavex):
    @staticmethod
    def from_bitarray(instr, processor):
        is_enterx = bit_at(instr, 4)
        return EnterxLeavexT1(instr, is_enterx=is_enterx)
