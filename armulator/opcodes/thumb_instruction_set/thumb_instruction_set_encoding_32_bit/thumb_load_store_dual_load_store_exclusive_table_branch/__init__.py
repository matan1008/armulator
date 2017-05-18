from strex_t1 import StrexT1
from ldrex_t1 import LdrexT1
from strd_immediate_t1 import StrdImmediateT1
from ldrd_immediate_t1 import LdrdImmediateT1
from ldrd_literal_t1 import LdrdLiteralT1
from strexb_t1 import StrexbT1
from strexh_t1 import StrexhT1
from strexd_t1 import StrexdT1
from tbb_t1 import TbbT1
from ldrexb_t1 import LdrexbT1
from ldrexh_t1 import LdrexhT1
from ldrexd_t1 import LdrexdT1


def decode_instruction(instr):
    if instr[7:9] == "0b00" and instr[10:12] == "0b00":
        # Store Register Exclusive
        return StrexT1
    elif instr[7:9] == "0b00" and instr[10:12] == "0b01":
        # Load Register Exclusive
        return LdrexT1
    elif (not instr[7] and instr[10:12] == "0b10") or (instr[7] and not instr[11]):
        # Store Register Dual
        return StrdImmediateT1
    elif instr[12:16] != "0b1111" and ((not instr[7] and instr[10:12] == "0b11") or (instr[7] and instr[11])):
        # Load Register Dual (immediate)
        return LdrdImmediateT1
    elif instr[12:16] == "0b1111" and ((not instr[7] and instr[10:12] == "0b11") or (instr[7] and instr[11])):
        # Load Register Dual (literal)
        return LdrdLiteralT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b00" and instr[24:28] == "0b0100":
        # Store Register Exclusive Byte
        return StrexbT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b00" and instr[24:28] == "0b0101":
        # Store Register Exclusive Halfword
        return StrexhT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b00" and instr[24:28] == "0b0111":
        # Store Register Exclusive Doubleword
        return StrexdT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b01" and (instr[24:28] == "0b0000" or instr[24:28] == "0b0001"):
        # Table Branch Byte / Table Branch Halfword
        return TbbT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b01" and instr[24:28] == "0b0100":
        # Load Register Exclusive Byte
        return LdrexbT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b01" and instr[24:28] == "0b0101":
        # Load Register Exclusive Halfword
        return LdrexhT1
    elif instr[7:9] == "0b01" and instr[10:12] == "0b01" and instr[24:28] == "0b0111":
        # Load Register Exclusive Doubleword
        return LdrexdT1
