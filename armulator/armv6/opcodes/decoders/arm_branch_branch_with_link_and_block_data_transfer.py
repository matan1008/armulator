from armulator.armv6.bits_ops import substring, bit_at, bit_count
from armulator.armv6.opcodes.concrete.b_a1 import BA1
from armulator.armv6.opcodes.concrete.bl_immediate_a1 import BlBlxImmediateA1
from armulator.armv6.opcodes.concrete.ldm_arm_a1 import LdmArmA1
from armulator.armv6.opcodes.concrete.ldm_exception_return_a1 import LdmExceptionReturnA1
from armulator.armv6.opcodes.concrete.ldm_user_registers_a1 import LdmUserRegistersA1
from armulator.armv6.opcodes.concrete.ldmda_a1 import LdmdaA1
from armulator.armv6.opcodes.concrete.ldmdb_a1 import LdmdbA1
from armulator.armv6.opcodes.concrete.ldmib_a1 import LdmibA1
from armulator.armv6.opcodes.concrete.pop_arm_a1 import PopArmA1
from armulator.armv6.opcodes.concrete.push_a1 import PushA1
from armulator.armv6.opcodes.concrete.stm_a1 import StmA1
from armulator.armv6.opcodes.concrete.stm_user_registers_a1 import StmUserRegistersA1
from armulator.armv6.opcodes.concrete.stmda_a1 import StmdaA1
from armulator.armv6.opcodes.concrete.stmdb_a1 import StmdbA1
from armulator.armv6.opcodes.concrete.stmib_a1 import StmibA1


def decode_instruction(instr):
    instr_25_22 = substring(instr, 25, 22)
    instr_20 = bit_at(instr, 20)
    op = substring(instr, 25, 20)
    rn = substring(instr, 19, 16)
    r = bit_at(instr, 15)
    instr_25_24 = substring(instr, 25, 24)
    instr_25 = bit_at(instr, 25)
    instr_22 = bit_at(instr, 22)
    register_list = substring(instr, 15, 0)
    if instr_25_22 == 0b0000 and not instr_20:
        # Store Multiple Decrement After
        return StmdaA1
    elif instr_25_22 == 0b0000 and instr_20:
        # Load Multiple Decrement After
        return LdmdaA1
    elif instr_25_22 == 0b0010 and not instr_20:
        # Store Multiple Increment After
        return StmA1
    elif op == 0b001001 or (op == 0b001011 and rn != 0b1101):
        # Load Multiple Increment After
        return LdmArmA1
    elif op == 0b001011 and rn == 0b1101:
        if bit_count(register_list, 1, 16) < 2:
            # Load Multiple Increment After
            return LdmArmA1
        else:
            # Pop multiple registers
            return PopArmA1
    elif op == 0b010000 or (op == 0b010010 and rn != 0b1101):
        # Store Multiple Decrement Before
        return StmdbA1
    elif op == 0b010010 and rn == 0b1101:
        if bit_count(register_list, 1, 16) < 2:
            # Store Multiple Decrement Before
            return StmdbA1
        else:
            # Push multiple registers
            return PushA1
    elif instr_25_22 == 0b0100 and instr_20:
        # Load Multiple Decrement Before
        return LdmdbA1
    elif instr_25_22 == 0b0110 and not instr_20:
        # Store Multiple Increment Before
        return StmibA1
    elif instr_25_22 == 0b0110 and instr_20:
        # Load Multiple Increment Before
        return LdmibA1
    elif not instr_25 and instr_22 and not instr_20:
        # Store Multiple (user registers)
        return StmUserRegistersA1
    elif not instr_25 and instr_22 and instr_20 and not r:
        # Load Multiple (user registers)
        return LdmUserRegistersA1
    elif not instr_25 and instr_22 and instr_20 and r:
        # Load Multiple (exception return)
        return LdmExceptionReturnA1
    elif instr_25_24 == 0b10:
        # Branch
        return BA1
    elif instr_25_24 == 0b11:
        # Branch with Link
        return BlBlxImmediateA1
