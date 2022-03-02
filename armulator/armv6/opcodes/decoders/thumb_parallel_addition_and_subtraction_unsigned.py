from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.uadd16_t1 import Uadd16T1
from armulator.armv6.opcodes.concrete.uadd8_t1 import Uadd8T1
from armulator.armv6.opcodes.concrete.uasx_t1 import UasxT1
from armulator.armv6.opcodes.concrete.uhadd16_t1 import Uhadd16T1
from armulator.armv6.opcodes.concrete.uhadd8_t1 import Uhadd8T1
from armulator.armv6.opcodes.concrete.uhasx_t1 import UhasxT1
from armulator.armv6.opcodes.concrete.uhsax_t1 import UhsaxT1
from armulator.armv6.opcodes.concrete.uhsub16_t1 import Uhsub16T1
from armulator.armv6.opcodes.concrete.uhsub8_t1 import Uhsub8T1
from armulator.armv6.opcodes.concrete.uqadd16_t1 import Uqadd16T1
from armulator.armv6.opcodes.concrete.uqadd8_t1 import Uqadd8T1
from armulator.armv6.opcodes.concrete.uqasx_t1 import UqasxT1
from armulator.armv6.opcodes.concrete.uqsax_t1 import UqsaxT1
from armulator.armv6.opcodes.concrete.uqsub16_t1 import Uqsub16T1
from armulator.armv6.opcodes.concrete.uqsub8_t1 import Uqsub8T1
from armulator.armv6.opcodes.concrete.usax_t1 import UsaxT1
from armulator.armv6.opcodes.concrete.usub16_t1 import Usub16T1
from armulator.armv6.opcodes.concrete.usub8_t1 import Usub8T1


def decode_instruction(instr):
    op1 = substring(instr, 22, 20)
    op2 = substring(instr, 5, 4)
    if op1 == 0b001 and op2 == 0b00:
        # Add 16-bit
        return Uadd16T1
    elif op1 == 0b010 and op2 == 0b00:
        # Add and Subtract with Exchange, 16-bit
        return UasxT1
    elif op1 == 0b110 and op2 == 0b00:
        # Subtract and Add with Exchange, 16-bit
        return UsaxT1
    elif op1 == 0b101 and op2 == 0b00:
        # Subtract 16-bit
        return Usub16T1
    elif op1 == 0b000 and op2 == 0b00:
        # Add 8-bit
        return Uadd8T1
    elif op1 == 0b100 and op2 == 0b00:
        # Subtract 8-bit
        return Usub8T1
    elif op1 == 0b001 and op2 == 0b01:
        # Saturating Add 16-bit
        return Uqadd16T1
    elif op1 == 0b010 and op2 == 0b01:
        # Saturating Add and Subtract with Exchange, 16-bit
        return UqasxT1
    elif op1 == 0b110 and op2 == 0b01:
        # Saturating Subtract and Add with Exchange, 16-bit
        return UqsaxT1
    elif op1 == 0b101 and op2 == 0b01:
        # Saturating Subtract 16-bit
        return Uqsub16T1
    elif op1 == 0b000 and op2 == 0b01:
        # Saturating Add 8-bit
        return Uqadd8T1
    elif op1 == 0b100 and op2 == 0b01:
        # Saturating Subtract 8-bit
        return Uqsub8T1
    elif op1 == 0b001 and op2 == 0b10:
        # Halving Add 16-bit
        return Uhadd16T1
    elif op1 == 0b010 and op2 == 0b10:
        # Halving Add and Subtract with Exchange, 16-bit
        return UhasxT1
    elif op1 == 0b110 and op2 == 0b10:
        # Halving Subtract and Add with Exchange, 16-bit
        return UhsaxT1
    elif op1 == 0b101 and op2 == 0b10:
        # Halving Subtract 16-bit
        return Uhsub16T1
    elif op1 == 0b000 and op2 == 0b10:
        # Halving Add 8-bit
        return Uhadd8T1
    elif op1 == 0b100 and op2 == 0b10:
        # Halving Subtract 8-bit
        return Uhsub8T1
