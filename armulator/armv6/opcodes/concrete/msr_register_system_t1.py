from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.abstract_opcodes.msr_register_system import MsrRegisterSystem


class MsrRegisterSystemT1(MsrRegisterSystem):
    @staticmethod
    def from_bitarray(instr, processor):
        mask = substring(instr, 11, 8)
        rn = substring(instr, 19, 16)
        write_spsr = bit_at(instr, 20)
        if mask == 0b0000 or rn in (13, 15):
            print('unpredictable')
        else:
            return MsrRegisterSystemT1(instr, write_spsr=write_spsr, mask=mask, n=rn)
