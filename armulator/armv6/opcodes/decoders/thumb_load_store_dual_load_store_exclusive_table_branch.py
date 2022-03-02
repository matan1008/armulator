from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldrd_immediate_t1 import LdrdImmediateT1
from armulator.armv6.opcodes.concrete.ldrd_literal_t1 import LdrdLiteralT1
from armulator.armv6.opcodes.concrete.ldrex_t1 import LdrexT1
from armulator.armv6.opcodes.concrete.ldrexb_t1 import LdrexbT1
from armulator.armv6.opcodes.concrete.ldrexd_t1 import LdrexdT1
from armulator.armv6.opcodes.concrete.ldrexh_t1 import LdrexhT1
from armulator.armv6.opcodes.concrete.strd_immediate_t1 import StrdImmediateT1
from armulator.armv6.opcodes.concrete.strex_t1 import StrexT1
from armulator.armv6.opcodes.concrete.strexb_t1 import StrexbT1
from armulator.armv6.opcodes.concrete.strexd_t1 import StrexdT1
from armulator.armv6.opcodes.concrete.strexh_t1 import StrexhT1
from armulator.armv6.opcodes.concrete.tbb_tbh_t1 import TbbTbhT1


def decode_instruction(instr):
    instr_op1 = substring(instr, 24, 23)
    instr_op2 = substring(instr, 21, 20)
    instr_op3 = substring(instr, 7, 4)
    instr_rn = substring(instr, 19, 16)
    instr_24 = bit_at(instr, 24)
    instr_20 = bit_at(instr, 20)
    if instr_op1 == 0b00 and instr_op2 == 0b00:
        # Store Register Exclusive
        return StrexT1
    elif instr_op1 == 0b00 and instr_op2 == 0b01:
        # Load Register Exclusive
        return LdrexT1
    elif (not instr_24 and instr_op2 == 0b10) or (instr_24 and not instr_20):
        # Store Register Dual
        return StrdImmediateT1
    elif instr_rn != 0b1111 and ((not instr_24 and instr_op2 == 0b11) or (instr_24 and instr_20)):
        # Load Register Dual (immediate)
        return LdrdImmediateT1
    elif instr_rn == 0b1111 and ((not instr_24 and instr_op2 == 0b11) or (instr_24 and instr_20)):
        # Load Register Dual (literal)
        return LdrdLiteralT1
    elif instr_op1 == 0b01 and instr_op2 == 0b00 and instr_op3 == 0b0100:
        # Store Register Exclusive Byte
        return StrexbT1
    elif instr_op1 == 0b01 and instr_op2 == 0b00 and instr_op3 == 0b0101:
        # Store Register Exclusive Halfword
        return StrexhT1
    elif instr_op1 == 0b01 and instr_op2 == 0b00 and instr_op3 == 0b0111:
        # Store Register Exclusive Doubleword
        return StrexdT1
    elif instr_op1 == 0b01 and instr_op2 == 0b01 and (instr_op3 == 0b0000 or instr_op3 == 0b0001):
        # Table Branch Byte / Table Branch Halfword
        return TbbTbhT1
    elif instr_op1 == 0b01 and instr_op2 == 0b01 and instr_op3 == 0b0100:
        # Load Register Exclusive Byte
        return LdrexbT1
    elif instr_op1 == 0b01 and instr_op2 == 0b01 and instr_op3 == 0b0101:
        # Load Register Exclusive Halfword
        return LdrexhT1
    elif instr_op1 == 0b01 and instr_op2 == 0b01 and instr_op3 == 0b0111:
        # Load Register Exclusive Doubleword
        return LdrexdT1
