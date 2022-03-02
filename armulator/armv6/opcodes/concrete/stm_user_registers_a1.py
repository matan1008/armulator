from armulator.armv6.bits_ops import substring, bit_at, bit_count
from armulator.armv6.opcodes.abstract_opcodes.stm_user_registers import StmUserRegisters


class StmUserRegistersA1(StmUserRegisters):
    @staticmethod
    def from_bitarray(instr, processor):
        register_list = substring(instr, 15, 0)
        rn = substring(instr, 19, 16)
        increment = bit_at(instr, 23)
        word_higher = increment == bit_at(instr, 24)
        if rn == 15 or bit_count(register_list, 1, 16) < 1:
            print('unpredictable')
        else:
            return StmUserRegistersA1(instr, increment=increment, word_higher=word_higher, registers=register_list,
                                      n=rn)
