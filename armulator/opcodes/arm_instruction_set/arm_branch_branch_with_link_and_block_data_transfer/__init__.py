from stmda_a1 import StmdaA1
from ldmda_a1 import LdmdaA1
from stm_a1 import StmA1
from ldm_arm_a1 import LdmArmA1
from pop_arm_a1 import PopArmA1
from stmdb_a1 import StmdbA1
from push_a1 import PushA1
from ldmdb_a1 import LdmdbA1
from stmib_a1 import StmibA1
from ldmib_a1 import LdmibA1
from stm_user_registers_a1 import StmUserRegistersA1
from ldm_user_registers_a1 import LdmUserRegistersA1
from ldm_exception_return_a1 import LdmExceptionReturnA1
from b_a1 import BA1
from bl_immediate_a1 import BlImmediateA1


def decode_instruction(instr):
    if instr[6:10] == "0b0000" and not instr[11]:
        # Store Multiple Decrement After
        return StmdaA1
    elif instr[6:10] == "0b0000" and instr[11]:
        # Load Multiple Decrement After
        return LdmdaA1
    elif instr[6:10] == "0b0010" and not instr[11]:
        # Store Multiple Increment After
        return StmA1
    elif instr[6:12] == "0b001001" or (instr[6:12] == "0b001011" and instr[12:16] != "0b1101"):
        # Load Multiple Increment After
        return LdmArmA1
    elif instr[6:12] == "0b001011" and instr[12:16] == "0b1101":
        if instr[16:32].count(1) < 2:
            # Load Multiple Increment After
            return LdmArmA1
        else:
            # Pop multiple registers
            return PopArmA1
    elif instr[6:12] == "0b010000" or (instr[6:12] == "0b010010" and instr[12:16] != "0b1101"):
        # Store Multiple Decrement Before
        return StmdbA1
    elif instr[6:12] == "0b010010" and instr[12:16] == "0b1101":
        if instr[16:32].count(1) < 2:
            # Store Multiple Decrement Before
            return StmdbA1
        else:
            # Push multiple registers
            return PushA1
    elif instr[6:10] == "0b0100" and instr[11]:
        # Load Multiple Decrement Before
        return LdmdbA1
    elif instr[6:10] == "0b0110" and not instr[11]:
        # Store Multiple Increment Before
        return StmibA1
    elif instr[6:10] == "0b0110" and instr[11]:
        # Load Multiple Increment Before
        return LdmibA1
    elif not instr[6] and instr[9] and not instr[11]:
        # Store Multiple (user registers)
        return StmUserRegistersA1
    elif not instr[6] and instr[9] and not instr[11] and not instr[16]:
        # Load Multiple (user registers)
        return LdmUserRegistersA1
    elif not instr[6] and instr[9] and not instr[11] and instr[16]:
        # Load Multiple (exception return)
        return LdmExceptionReturnA1
    elif instr[6:8] == "0b10":
        # Branch
        return BA1
    elif instr[6:8] == "0b11":
        # Branch with Link
        return BlImmediateA1
