from srs_thumb_t1 import SrsThumbT1
from rfe_t1 import RfeT1
from stm_t2 import StmT2
from ldm_thumb_t2 import LdmThumbT2
from pop_thumb_t2 import PopThumbT2
from stmdb_t1 import StmdbT1
from push_t2 import PushT2
from ldmdb_t1 import LdmdbT1
from srs_thumb_t2 import SrsThumbT2
from rfe_t2 import RfeT2


def decode_instruction(instr):
    if instr[7:9] == "0b00" and not instr[11]:
        # Store Return State
        return SrsThumbT1
    elif instr[7:9] == "0b00" and instr[11]:
        # Return From Exception
        return RfeT1
    elif instr[7:9] == "0b01" and not instr[11]:
        # Store Multiple (Increment After, Empty Ascending)
        return StmT2
    elif instr[7:9] == "0b01" and instr[11] and (instr[10:11] + instr[12:16] != "0b11101"):
        # Load Multiple (Increment After, Full Descending)
        return LdmThumbT2
    elif instr[7:9] == "0b01" and instr[11] and (instr[10:11] + instr[12:16] == "0b11101"):
        # Pop Multiple Registers from the stack
        return PopThumbT2
    elif instr[7:9] == "0b10" and not instr[11] and (instr[10:11] + instr[12:16] != "0b11101"):
        # Store Multiple (Decrement Before, Full Descending)
        return StmdbT1
    elif instr[7:9] == "0b10" and not instr[11] and (instr[10:11] + instr[12:16] == "0b11101"):
        # Push Multiple Registers to the stack.
        return PushT2
    elif instr[7:9] == "0b10" and instr[11]:
        # Load Multiple (Decrement Before, Empty Ascending)
        return LdmdbT1
    elif instr[7:9] == "0b11" and not instr[11]:
        # Store Return State
        return SrsThumbT2
    elif instr[7:9] == "0b11" and instr[11]:
        # Return From Exception
        return RfeT2
