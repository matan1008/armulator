from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.ldrex_a1 import LdrexA1
from armulator.armv6.opcodes.concrete.ldrexb_a1 import LdrexbA1
from armulator.armv6.opcodes.concrete.ldrexd_a1 import LdrexdA1
from armulator.armv6.opcodes.concrete.ldrexh_a1 import LdrexhA1
from armulator.armv6.opcodes.concrete.strex_a1 import StrexA1
from armulator.armv6.opcodes.concrete.strexb_a1 import StrexbA1
from armulator.armv6.opcodes.concrete.strexd_a1 import StrexdA1
from armulator.armv6.opcodes.concrete.strexh_a1 import StrexhA1


def decode_instruction(instr):
    op = substring(instr, 23, 20)
    if op in (0b0000, 0b0100):
        # Swap Word, Swap Byte
        print('deprecated')
    elif op == 0b1000:
        # Store Register Exclusive
        return StrexA1
    elif op == 0b1001:
        # Load Register Exclusive
        return LdrexA1
    elif op == 0b1010:
        # Store Register Exclusive Doubleword
        return StrexdA1
    elif op == 0b1011:
        # Load Register Exclusive Doubleword
        return LdrexdA1
    elif op == 0b1100:
        # Store Register Exclusive Byte
        return StrexbA1
    elif op == 0b1101:
        # Load Register Exclusive Byte
        return LdrexbA1
    elif op == 0b1110:
        # Store Register Exclusive Halfword
        return StrexhA1
    elif op == 0b1111:
        # Load Register Exclusive Halfword
        return LdrexhA1
