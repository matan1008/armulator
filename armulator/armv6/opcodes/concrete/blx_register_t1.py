from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.blx_register import BlxRegister


class BlxRegisterT1(BlxRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 6, 3)
        if rm == 15 or (processor.in_it_block() and not processor.last_in_it_block()):
            print('unpredictable')
        else:
            return BlxRegisterT1(instr, m=rm)
