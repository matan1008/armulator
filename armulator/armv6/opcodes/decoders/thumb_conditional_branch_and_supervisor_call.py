from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.b_t1 import BT1
from armulator.armv6.opcodes.concrete.svc_t1 import SvcT1
from armulator.armv6.opcodes.concrete.udf_t1 import UdfT1


def decode_instruction(instr):
    if substring(instr, 11, 9) != 0b111:
        # Conditional branch
        return BT1
    elif substring(instr, 11, 8) == 0b1110:
        # Permanently UNDEFINED
        return UdfT1
    elif substring(instr, 11, 8) == 0b1111:
        # Supervisor Call
        return SvcT1
