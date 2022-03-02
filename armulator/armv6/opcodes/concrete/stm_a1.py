from armulator.armv6.bits_ops import substring, bit_at, bit_count
from armulator.armv6.opcodes.abstract_opcodes.stm import Stm


class StmA1(Stm):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 15, 0)
        rn = substring(instr, 19, 16)
        wback = bit_at(instr, 21)
        if rn == 15 or bit_count(register_list, 1, 16) < 1:
            print('unpredictable')
        else:
            return StmA1(instr, wback=wback, registers=register_list, n=rn)
