from qadd_t1 import QaddT1
from qdadd_t1 import QdaddT1
from qsub_t1 import QsubT1
from qdsub_t1 import QdsubT1
from rev_t2 import RevT2
from rev16_t2 import Rev16T2
from rbit_t1 import RbitT1
from revsh_t2 import RevshT2
from sel_t1 import SelT1
from clz_t1 import ClzT1


def decode_instruction(instr):
    if instr[10:12] == "0b00" and instr[26:28] == "0b00":
        # Saturating Add
        return QaddT1
    elif instr[10:12] == "0b00" and instr[26:28] == "0b01":
        # Saturating Double and Add
        return QdaddT1
    elif instr[10:12] == "0b00" and instr[26:28] == "0b10":
        # Saturating Subtract
        return QsubT1
    elif instr[10:12] == "0b00" and instr[26:28] == "0b11":
        # Saturating Double and Subtract
        return QdsubT1
    elif instr[10:12] == "0b01" and instr[26:28] == "0b00":
        # Byte-Reverse Word
        return RevT2
    elif instr[10:12] == "0b01" and instr[26:28] == "0b01":
        # Byte-Reverse Packed Halfword
        return Rev16T2
    elif instr[10:12] == "0b01" and instr[26:28] == "0b10":
        # Reverse Bits
        return RbitT1
    elif instr[10:12] == "0b01" and instr[26:28] == "0b11":
        # Byte-Reverse Signed Halfword
        return RevshT2
    elif instr[10:12] == "0b10" and instr[26:28] == "0b00":
        # Select Bytes
        return SelT1
    elif instr[10:12] == "0b11" and instr[26:28] == "0b00":
        # Count Leading Zeros
        return ClzT1
