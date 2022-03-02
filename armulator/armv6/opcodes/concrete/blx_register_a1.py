from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.blx_register import BlxRegister


class BlxRegisterA1(BlxRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        if rm == 15:
            print('unpredictable')
        else:
            return BlxRegisterA1(instr, m=rm)
