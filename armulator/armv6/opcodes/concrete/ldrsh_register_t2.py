from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.abstract_opcodes.ldrsh_register import LdrshRegister
from armulator.armv6.shift import SRType


class LdrshRegisterT2(LdrshRegister):
    @staticmethod
    def from_bitarray(instr, processor):
        rm = substring(instr, 3, 0)
        imm2 = substring(instr, 5, 4)
        rt = substring(instr, 15, 12)
        rn = substring(instr, 19, 16)
        index = True
        add = True
        wback = False
        if rt == 13 or rm in (13, 15):
            print('unpredictable')
        else:
            return LdrshRegisterT2(instr, add=add, wback=wback, index=index, m=rm, t=rt, n=rn, shift_t=SRType.LSL,
                                   shift_n=imm2)
