from pkhbt_a1 import PkhbtA1
from sxtab16_a1 import Sxtab16A1
from sxtb16_a1 import Sxtb16A1
from sel_a1 import SelA1
from ssat_a1 import SsatA1
from ssat16_a1 import Ssat16A1
from sxtab_a1 import SxtabA1
from sxtb_a1 import SxtbA1
from rev_a1 import RevA1
from sxtah_a1 import SxtahA1
from sxth_a1 import SxthA1
from rev16_a1 import Rev16A1
from uxtab16_a1 import Uxtab16A1
from uxtb16_a1 import Uxtb16A1
from usat_a1 import UsatA1
from usat16_a1 import Usat16A1
from uxtab_a1 import UxtabA1
from uxtb_a1 import UxtbA1
from rbit_a1 import RbitA1
from uxtah_a1 import UxtahA1
from uxth_a1 import UxthA1
from revsh_a1 import RevshA1


def decode_instruction(instr):
    if instr[9:12] == "0b000" and not instr[26]:
        # Pack Halfword
        return PkhbtA1
    elif instr[9:12] == "0b000" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Signed Extend and Add Byte 16-bit
        return Sxtab16A1
    elif instr[9:12] == "0b000" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Signed Extend Byte 16-bit
        return Sxtb16A1
    elif instr[9:12] == "0b000" and instr[24:27] == "0b101":
        # Select Bytes
        return SelA1
    elif instr[9:11] == "0b01" and not instr[26]:
        # Signed Saturate
        return SsatA1
    elif instr[9:12] == "0b010" and instr[24:27] == "0b001":
        # Signed Saturate, two 16-bit
        return Ssat16A1
    elif instr[9:12] == "0b010" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Signed Extend and Add Byte
        return SxtabA1
    elif instr[9:12] == "0b010" and instr[24:27] == "0b011" and instr[12:16] == "0b1111":
        # Signed Extend Byte
        return SxtbA1
    elif instr[9:12] == "0b011" and instr[24:27] == "0b001":
        # Byte-Reverse Word
        return RevA1
    elif instr[9:12] == "0b011" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Signed Extend and Add Halfword
        return SxtahA1
    elif instr[9:12] == "0b011" and instr[24:27] == "0b011" and instr[12:16] == "0b1111":
        # Signed Extend Halfword
        return SxthA1
    elif instr[9:12] == "0b011" and instr[24:27] == "0b101":
        # Byte-Reverse Packed Halfword
        return Rev16A1
    elif instr[9:12] == "0b100" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Byte 16-bit
        return Uxtab16A1
    elif instr[9:12] == "0b100" and instr[24:27] == "0b011" and instr[12:16] == "0b1111":
        # Unsigned Extend Byte 16-bit
        return Uxtb16A1
    elif instr[9:11] == "0b11" and not instr[26]:
        # Unsigned Saturate
        return UsatA1
    elif instr[9:12] == "0b110" and instr[24:27] == "0b001":
        # Unsigned Saturate, two 16-bit
        return Usat16A1
    elif instr[9:12] == "0b110" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Byte
        return UxtabA1
    elif instr[9:12] == "0b110" and instr[24:27] == "0b011" and instr[12:16] == "0b1111":
        # Unsigned Extend Byte
        return UxtbA1
    elif instr[9:12] == "0b111" and instr[24:27] == "0b001":
        # Reverse Bits
        return RbitA1
    elif instr[9:12] == "0b111" and instr[24:27] == "0b011" and instr[12:16] != "0b1111":
        # Unsigned Extend and Add Halfword
        return UxtahA1
    elif instr[9:12] == "0b111" and instr[24:27] == "0b011" and instr[12:16] == "0b1111":
        # Unsigned Extend Byte
        return UxthA1
    elif instr[9:12] == "0b111" and instr[24:27] == "0b101":
        # Byte-Reverse Signed Halfword
        return RevshA1
