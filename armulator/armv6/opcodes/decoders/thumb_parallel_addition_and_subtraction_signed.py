from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.qadd16_t1 import Qadd16T1
from armulator.armv6.opcodes.concrete.qadd8_t1 import Qadd8T1
from armulator.armv6.opcodes.concrete.qasx_t1 import QasxT1
from armulator.armv6.opcodes.concrete.qsax_t1 import QsaxT1
from armulator.armv6.opcodes.concrete.qsub16_t1 import Qsub16T1
from armulator.armv6.opcodes.concrete.qsub8_t1 import Qsub8T1
from armulator.armv6.opcodes.concrete.sadd16_t1 import Sadd16T1
from armulator.armv6.opcodes.concrete.sadd8_t1 import Sadd8T1
from armulator.armv6.opcodes.concrete.sasx_t1 import SasxT1
from armulator.armv6.opcodes.concrete.shadd16_t1 import Shadd16T1
from armulator.armv6.opcodes.concrete.shadd8_t1 import Shadd8T1
from armulator.armv6.opcodes.concrete.shasx_t1 import ShasxT1
from armulator.armv6.opcodes.concrete.shsax_t1 import ShsaxT1
from armulator.armv6.opcodes.concrete.shsub16_t1 import Shsub16T1
from armulator.armv6.opcodes.concrete.shsub8_t1 import Shsub8T1
from armulator.armv6.opcodes.concrete.ssax_t1 import SsaxT1
from armulator.armv6.opcodes.concrete.ssub16_t1 import Ssub16T1
from armulator.armv6.opcodes.concrete.ssub8_t1 import Ssub8T1


def decode_instruction(instr):
    op1 = substring(instr, 22, 20)
    op2 = substring(instr, 5, 4)
    if op1 == 0b001 and op2 == 0b00:
        # Add 16-bit
        return Sadd16T1
    elif op1 == 0b010 and op2 == 0b00:
        # Add and Subtract with Exchange, 16-bit
        return SasxT1
    elif op1 == 0b110 and op2 == 0b00:
        # Subtract and Add with Exchange, 16-bit
        return SsaxT1
    elif op1 == 0b101 and op2 == 0b00:
        # Subtract 16-bit
        return Ssub16T1
    elif op1 == 0b000 and op2 == 0b00:
        # Add 8-bit
        return Sadd8T1
    elif op1 == 0b100 and op2 == 0b00:
        # Subtract 8-bit
        return Ssub8T1
    elif op1 == 0b001 and op2 == 0b01:
        # Saturating Add 16-bit
        return Qadd16T1
    elif op1 == 0b010 and op2 == 0b01:
        # Saturating Add and Subtract with Exchange, 16-bit
        return QasxT1
    elif op1 == 0b110 and op2 == 0b01:
        # Saturating Subtract and Add with Exchange, 16-bit
        return QsaxT1
    elif op1 == 0b101 and op2 == 0b01:
        # Saturating Subtract 16-bit
        return Qsub16T1
    elif op1 == 0b000 and op2 == 0b01:
        # Saturating Add 8-bit
        return Qadd8T1
    elif op1 == 0b100 and op2 == 0b01:
        # Saturating Subtract 8-bit
        return Qsub8T1
    elif op1 == 0b001 and op2 == 0b10:
        # Halving Add 16-bit
        return Shadd16T1
    elif op1 == 0b010 and op2 == 0b10:
        # Halving Add and Subtract with Exchange, 16-bit
        return ShasxT1
    elif op1 == 0b110 and op2 == 0b10:
        # Halving Subtract and Add with Exchange, 16-bit
        return ShsaxT1
    elif op1 == 0b101 and op2 == 0b10:
        # Halving Subtract 16-bit
        return Shsub16T1
    elif op1 == 0b000 and op2 == 0b10:
        # Halving Add 8-bit
        return Shadd8T1
    elif op1 == 0b100 and op2 == 0b10:
        # Halving Subtract 8-bit
        return Shsub8T1
