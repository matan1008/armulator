from armulator.armv6.bits_ops import substring, bit_at, chain, bit_count
from armulator.armv6.opcodes.abstract_opcodes.stm import Stm


class StmT2(Stm):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 12, 0)
        m = bit_at(instr, 14)
        wback = bit_at(instr, 21)
        rn = substring(instr, 19, 16)
        registers = chain(m, register_list, 14)
        if rn == 15 or bit_count(registers, 1, 16) < 2 or (wback and bit_at(registers, rn)):
            print('unpredictable')
        else:
            return StmT2(instr, wback=wback, registers=registers, n=rn)
