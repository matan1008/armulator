from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.sdiv_t1 import SdivT1
from armulator.armv6.opcodes.concrete.smlal_t1 import SmlalT1
from armulator.armv6.opcodes.concrete.smlald_t1 import SmlaldT1
from armulator.armv6.opcodes.concrete.smlalxy_t1 import SmlalxyT1
from armulator.armv6.opcodes.concrete.smlsld_t1 import SmlsldT1
from armulator.armv6.opcodes.concrete.smull_t1 import SmullT1
from armulator.armv6.opcodes.concrete.udiv_t1 import UdivT1
from armulator.armv6.opcodes.concrete.umaal_t1 import UmaalT1
from armulator.armv6.opcodes.concrete.umlal_t1 import UmlalT1
from armulator.armv6.opcodes.concrete.umull_t1 import UmullT1


def decode_instruction(instr):
    op1 = substring(instr, 22, 20)
    op2 = substring(instr, 7, 4)
    if op1 == 0b000 and op2 == 0b0000:
        # Signed Multiply Long
        return SmullT1
    elif op1 == 0b001 and op2 == 0b1111:
        # Signed Divide
        return SdivT1
    elif op1 == 0b010 and op2 == 0b0000:
        # Unsigned Multiply Long
        return UmullT1
    elif op1 == 0b011 and op2 == 0b1111:
        # Unsigned Divide
        return UdivT1
    elif op1 == 0b100 and op2 == 0b0000:
        # Signed Multiply Accumulate Long
        return SmlalT1
    elif op1 == 0b100 and substring(instr, 7, 6) == 0b10:
        # Signed Multiply Accumulate Long (Halfwords)
        return SmlalxyT1
    elif op1 == 0b100 and substring(instr, 7, 5) == 0b110:
        # Signed Multiply Accumulate Long Dual
        return SmlaldT1
    elif op1 == 0b101 and substring(instr, 7, 5) == 0b110:
        # Signed Multiply Subtract Long Dual
        return SmlsldT1
    elif op1 == 0b110 and op2 == 0b0000:
        # Unsigned Multiply Accumulate Long
        return UmlalT1
    elif op1 == 0b110 and op2 == 0b0110:
        # Unsigned Multiply Accumulate Accumulate Long
        return UmaalT1
