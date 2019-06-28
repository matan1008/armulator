from __future__ import absolute_import
from . import thumb_shift_immediate_add_subtract_move_and_compare
from . import thumb_data_processing
from . import thumb_special_data_instructions_and_branch_and_exchange
from .ldr_literal_t1 import LdrLiteralT1
from . import thumb_load_store_single_data_item
from .adr_t1 import AdrT1
from .add_sp_plus_immediate_t1 import AddSpPlusImmediateT1
from . import thumb_miscellaneous_16_bit_instructions
from .stm_t1 import StmT1
from .ldm_thumb_t1 import LdmThumbT1
from . import thumb_conditional_branch_and_supervisor_call
from .b_t2 import BT2


def decode_instruction(instr):
    if instr[0:2] == "0b00":
        # Shift (immediate), add, subtract, move, and compare
        return thumb_shift_immediate_add_subtract_move_and_compare.decode_instruction(instr)
    elif instr[0:6] == "0b010000":
        # Data-processing
        return thumb_data_processing.decode_instruction(instr)
    elif instr[0:6] == "0b010001":
        # Special data instructions and branch and exchange
        return thumb_special_data_instructions_and_branch_and_exchange.decode_instruction(instr)
    elif instr[0:5] == "0b01001":
        # Load from Literal Pool
        return LdrLiteralT1
    elif instr[0:4] == "0b0101" or instr[0:3] == "0b011" or instr[0:3] == "0b100":
        # Load/store single data item
        return thumb_load_store_single_data_item.decode_instruction(instr)
    elif instr[0:5] == "0b10100":
        # Generate PC-relative address
        return AdrT1
    elif instr[0:5] == "0b10101":
        # Generate SP-relative address
        return AddSpPlusImmediateT1
    elif instr[0:4] == "0b1011":
        # Miscellaneous 16-bit instructions
        return thumb_miscellaneous_16_bit_instructions.decode_instruction(instr)
    elif instr[0:5] == "0b11000":
        # Store multiple registers
        return StmT1
    elif instr[0:5] == "0b11001":
        # Load multiple registers
        return LdmThumbT1
    elif instr[0:4] == "0b1101":
        # Conditional branch, and Supervisor Call
        return thumb_conditional_branch_and_supervisor_call.decode_instruction(instr)
    elif instr[0:5] == "0b11100":
        # Unconditional Branch
        return BT2
