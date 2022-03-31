from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldrht_a1 import LdrhtA1
from armulator.armv6.opcodes.concrete.ldrht_a2 import LdrhtA2
from armulator.armv6.opcodes.concrete.ldrsbt_a1 import LdrsbtA1
from armulator.armv6.opcodes.concrete.ldrsbt_a2 import LdrsbtA2
from armulator.armv6.opcodes.concrete.ldrsht_a1 import LdrshtA1
from armulator.armv6.opcodes.concrete.ldrsht_a2 import LdrshtA2
from armulator.armv6.opcodes.concrete.strht_a1 import StrhtA1
from armulator.armv6.opcodes.concrete.strht_a2 import StrhtA2


def decode_instruction(instr):
    op2 = substring(instr, 6, 5)
    op = bit_at(instr, 20)
    instr_22 = bit_at(instr, 22)
    if op2 == 0b01 and not op:
        # Store Halfword Unprivileged
        if instr_22:
            return StrhtA1
        else:
            return StrhtA2
    elif op2 == 0b01 and op:
        # Load Halfword Unprivileged
        if instr_22:
            return LdrhtA1
        else:
            return LdrhtA2
    elif op2 == 0b10 and op:
        # Load Signed Byte Unprivileged
        if instr_22:
            return LdrsbtA1
        else:
            return LdrsbtA2
    elif op2 == 0b11 and op:
        # Load Signed Halfword Unprivileged
        if instr_22:
            return LdrshtA1
        else:
            return LdrshtA2
