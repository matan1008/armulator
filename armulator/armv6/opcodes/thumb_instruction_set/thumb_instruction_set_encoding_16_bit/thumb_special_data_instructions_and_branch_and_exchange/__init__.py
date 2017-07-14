from add_sp_plus_register_thumb_t1 import AddSpPlusRegisterThumbT1
from add_sp_plus_register_thumb_t2 import AddSpPlusRegisterThumbT2
from add_register_thumb_t2 import AddRegisterThumbT2
from cmp_register_t2 import CmpRegisterT2
from mov_register_thumb_t1 import MovRegisterThumbT1
from bx_t1 import BxT1
from blx_register_t1 import BlxRegisterT1


def decode_instruction(instr):
    if instr[6:10] == "0b0000" or instr[6:10] == "0b0001" or instr[6:9] == "0b001":
        # Add Low Registers / Add High Registers
        if instr[9:13] == "0b1101":
            return AddSpPlusRegisterThumbT1
        elif instr[8:9] + instr[13:16] == "0b1101":
            return AddSpPlusRegisterThumbT2
        else:
            return AddRegisterThumbT2
    elif instr[6:8] == "0b01":
        # Compare High Registers
        return CmpRegisterT2
    elif instr[6:10] == "0b1000" or instr[6:10] == "0b1001" or instr[6:9] == "0b101":
        # Move Low Registers / Move High Registers
        return MovRegisterThumbT1
    elif instr[6:9] == "0b110":
        # Branch and Exchange
        return BxT1
    elif instr[6:9] == "0b111":
        # Branch with Link and Exchange
        return BlxRegisterT1
