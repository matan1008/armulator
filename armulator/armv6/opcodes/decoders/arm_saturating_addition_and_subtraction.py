from armulator.armv6.bits_ops import substring
from armulator.armv6.opcodes.concrete.qadd_a1 import QaddA1
from armulator.armv6.opcodes.concrete.qdadd_a1 import QdaddA1
from armulator.armv6.opcodes.concrete.qdsub_a1 import QdsubA1
from armulator.armv6.opcodes.concrete.qsub_a1 import QsubA1


def decode_instruction(instr):
    op = substring(instr, 22, 21)
    if op == 0b00:
        # Saturating Add
        return QaddA1
    elif op == 0b01:
        # Saturating Subtract
        return QsubA1
    elif op == 0b10:
        # Saturating Double and Add
        return QdaddA1
    elif op == 0b11:
        # Saturating Double and Subtract
        return QdsubA1
