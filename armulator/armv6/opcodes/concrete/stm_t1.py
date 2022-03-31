from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.stm import Stm


class StmT1(Stm):
    @staticmethod
    def from_bitarray(instr, processor):
        registers = substring(instr, 7, 0)
        rn = substring(instr, 10, 8)
        wback = True
        if not registers:
            print('unpredictable')
        else:
            return StmT1(instr, wback=wback, registers=registers, n=rn)
