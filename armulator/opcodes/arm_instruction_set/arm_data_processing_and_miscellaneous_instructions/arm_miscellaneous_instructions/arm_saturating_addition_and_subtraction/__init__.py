from qadd_a1 import QaddA1
from qsub_a1 import QsubA1
from qdadd_a1 import QdaddA1
from qdsub_a1 import QdsubA1


def decode_instruction(instr):
    if instr[9:11] == "0b00":
        # Saturating Add
        return QaddA1
    elif instr[9:11] == "0b01":
        # Saturating Subtract
        return QsubA1
    elif instr[9:11] == "0b10":
        # Saturating Double and Add
        return QdaddA1
    elif instr[9:11] == "0b11":
        # Saturating Double and Subtract
        return QdsubA1
