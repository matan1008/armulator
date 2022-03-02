from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.clz_t1 import ClzT1
from armulator.armv6.opcodes.concrete.qadd_t1 import QaddT1
from armulator.armv6.opcodes.concrete.qdadd_t1 import QdaddT1
from armulator.armv6.opcodes.concrete.qdsub_t1 import QdsubT1
from armulator.armv6.opcodes.concrete.qsub_t1 import QsubT1
from armulator.armv6.opcodes.concrete.rbit_t1 import RbitT1
from armulator.armv6.opcodes.concrete.rev16_t2 import Rev16T2
from armulator.armv6.opcodes.concrete.rev_t2 import RevT2
from armulator.armv6.opcodes.concrete.revsh_t2 import RevshT2
from armulator.armv6.opcodes.concrete.sel_t1 import SelT1


def decode_instruction(instr):
    op1 = substring(instr, 21, 20)
    op2 = substring(instr, 5, 4)
    if op1 == 0b00 and op2 == 0b00:
        # Saturating Add
        return QaddT1
    elif op1 == 0b00 and op2 == 0b01:
        # Saturating Double and Add
        return QdaddT1
    elif op1 == 0b00 and op2 == 0b10:
        # Saturating Subtract
        return QsubT1
    elif op1 == 0b00 and op2 == 0b11:
        # Saturating Double and Subtract
        return QdsubT1
    elif op1 == 0b01 and op2 == 0b00:
        # Byte-Reverse Word
        return RevT2
    elif op1 == 0b01 and op2 == 0b01:
        # Byte-Reverse Packed Halfword
        return Rev16T2
    elif op1 == 0b01 and op2 == 0b10:
        # Reverse Bits
        return RbitT1
    elif op1 == 0b01 and op2 == 0b11:
        # Byte-Reverse Signed Halfword
        return RevshT2
    elif op1 == 0b10 and op2 == 0b00:
        # Select Bytes
        return SelT1
    elif op1 == 0b11 and op2 == 0b00:
        # Count Leading Zeros
        return ClzT1
