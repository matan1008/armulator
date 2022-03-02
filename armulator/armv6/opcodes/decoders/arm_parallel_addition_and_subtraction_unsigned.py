from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.uadd16_a1 import Uadd16A1
from armulator.armv6.opcodes.concrete.uadd8_a1 import Uadd8A1
from armulator.armv6.opcodes.concrete.uasx_a1 import UasxA1
from armulator.armv6.opcodes.concrete.uhadd16_a1 import Uhadd16A1
from armulator.armv6.opcodes.concrete.uhadd8_a1 import Uhadd8A1
from armulator.armv6.opcodes.concrete.uhasx_a1 import UhasxA1
from armulator.armv6.opcodes.concrete.uhsax_a1 import UhsaxA1
from armulator.armv6.opcodes.concrete.uhsub16_a1 import Uhsub16A1
from armulator.armv6.opcodes.concrete.uhsub8_a1 import Uhsub8A1
from armulator.armv6.opcodes.concrete.uqadd16_a1 import Uqadd16A1
from armulator.armv6.opcodes.concrete.uqadd8_a1 import Uqadd8A1
from armulator.armv6.opcodes.concrete.uqasx_a1 import UqasxA1
from armulator.armv6.opcodes.concrete.uqsax_a1 import UqsaxA1
from armulator.armv6.opcodes.concrete.uqsub16_a1 import Uqsub16A1
from armulator.armv6.opcodes.concrete.uqsub8_a1 import Uqsub8A1
from armulator.armv6.opcodes.concrete.usax_a1 import UsaxA1
from armulator.armv6.opcodes.concrete.usub16_a1 import Usub16A1
from armulator.armv6.opcodes.concrete.usub8_a1 import Usub8A1


def decode_instruction(instr):
    op1 = substring(instr, 21, 20)
    op2 = substring(instr, 7, 5)
    if op1 == 0b01 and op2 == 0b000:
        # Add 16-bit
        return Uadd16A1
    elif op1 == 0b01 and op2 == 0b001:
        # Add and Subtract with Exchange, 16-bit
        return UasxA1
    elif op1 == 0b01 and op2 == 0b010:
        # Subtract and Add with Exchange, 16-bit
        return UsaxA1
    elif op1 == 0b01 and op2 == 0b011:
        # Subtract 16-bit
        return Usub16A1
    elif op1 == 0b01 and op2 == 0b100:
        # Add 8-bit
        return Uadd8A1
    elif op1 == 0b01 and op2 == 0b111:
        # Subtract 8-bit
        return Usub8A1
    elif op1 == 0b10 and op2 == 0b000:
        # Saturating Add 16-bit
        return Uqadd16A1
    elif op1 == 0b10 and op2 == 0b001:
        # Saturating Add and Subtract with Exchange, 16-bit
        return UqasxA1
    elif op1 == 0b10 and op2 == 0b010:
        # Saturating Subtract and Add with Exchange, 16-bit
        return UqsaxA1
    elif op1 == 0b10 and op2 == 0b011:
        # Saturating Subtract 16-bit
        return Uqsub16A1
    elif op1 == 0b10 and op2 == 0b100:
        # Saturating Add 8-bit
        return Uqadd8A1
    elif op1 == 0b10 and op2 == 0b111:
        # Saturating Subtract 8-bit
        return Uqsub8A1
    elif op1 == 0b11 and op2 == 0b000:
        # Halving Add 16-bit
        return Uhadd16A1
    elif op1 == 0b11 and op2 == 0b001:
        # Halving Add and Subtract with Exchange, 16-bit
        return UhasxA1
    elif op1 == 0b11 and op2 == 0b010:
        # Halving Subtract and Add with Exchange, 16-bit
        return UhsaxA1
    elif op1 == 0b11 and op2 == 0b011:
        # Halving Subtract 16-bit
        return Uhsub16A1
    elif op1 == 0b11 and op2 == 0b100:
        # Halving Add 8-bit
        return Uhadd8A1
    elif op1 == 0b11 and op2 == 0b111:
        # Halving Subtract 8-bit
        return Uhsub8A1
