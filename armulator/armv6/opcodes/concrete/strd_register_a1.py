from armulator.armv6.bits_ops import bit_at, substring
from armulator.armv6.configurations import arch_version
from armulator.armv6.opcodes.abstract_opcodes.strd_register import StrdRegister


class StrdRegisterA1(StrdRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        w = bit_at(instr, 21)
        index = bit_at(instr, 24)
        rm = substring(instr, 3, 0)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        add = bit_at(instr, 23)
        t2 = rt + 1
        wback = (not index) or w
        if bit_at(rt, 0) or (not index and w) or (t2 == 15 or rm == 15) or (
                wback and (rn == 15 or rn == rt or rn == t2)) or (arch_version() < 6 and wback and rn == rm):
            print('unpredictable')
        else:
            return StrdRegisterA1(instr, add=add, wback=wback, index=index, m=rm, t=rt, t2=t2, n=rn)
