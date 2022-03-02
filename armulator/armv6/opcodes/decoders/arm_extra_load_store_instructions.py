from armulator.armv6.bits_ops import substring, bit_at
from armulator.armv6.opcodes.concrete.ldrd_immediate_a1 import LdrdImmediateA1
from armulator.armv6.opcodes.concrete.ldrd_literal_a1 import LdrdLiteralA1
from armulator.armv6.opcodes.concrete.ldrd_register_a1 import LdrdRegisterA1
from armulator.armv6.opcodes.concrete.ldrh_immediate_arm_a1 import LdrhImmediateArmA1
from armulator.armv6.opcodes.concrete.ldrh_literal_a1 import LdrhLiteralA1
from armulator.armv6.opcodes.concrete.ldrh_register_a1 import LdrhRegisterA1
from armulator.armv6.opcodes.concrete.ldrsb_immediate_a1 import LdrsbImmediateA1
from armulator.armv6.opcodes.concrete.ldrsb_literal_a1 import LdrsbLiteralA1
from armulator.armv6.opcodes.concrete.ldrsb_register_a1 import LdrsbRegisterA1
from armulator.armv6.opcodes.concrete.ldrsbt_a1 import LdrsbtA1
from armulator.armv6.opcodes.concrete.ldrsbt_a2 import LdrsbtA2
from armulator.armv6.opcodes.concrete.ldrsh_immediate_a1 import LdrshImmediateA1
from armulator.armv6.opcodes.concrete.ldrsh_literal_a1 import LdrshLiteralA1
from armulator.armv6.opcodes.concrete.ldrsh_register_a1 import LdrshRegisterA1
from armulator.armv6.opcodes.concrete.ldrsht_a1 import LdrshtA1
from armulator.armv6.opcodes.concrete.ldrsht_a2 import LdrshtA2
from armulator.armv6.opcodes.concrete.strd_immediate_a1 import StrdImmediateA1
from armulator.armv6.opcodes.concrete.strd_register_a1 import StrdRegisterA1
from armulator.armv6.opcodes.concrete.strh_immediate_arm_a1 import StrhImmediateArmA1
from armulator.armv6.opcodes.concrete.strh_register_a1 import StrhRegisterA1


def decode_instruction(instr):
    op2 = substring(instr, 6, 5)
    rn = substring(instr, 19, 16)
    instr_22 = bit_at(instr, 22)
    instr_20 = bit_at(instr, 20)
    instr_24 = bit_at(instr, 24)
    instr_21 = bit_at(instr, 21)
    if op2 == 0b01 and not instr_22 and not instr_20:
        # Store Halfword register
        return StrhRegisterA1
    elif op2 == 0b01 and not instr_22 and instr_20:
        # Load Halfword register
        return LdrhRegisterA1
    elif op2 == 0b01 and instr_22 and not instr_20:
        # Store Halfword immediate arm
        return StrhImmediateArmA1
    elif op2 == 0b01 and instr_22 and instr_20 and rn != 0b1111:
        # Load Halfword immediate arm
        return LdrhImmediateArmA1
    elif op2 == 0b01 and instr_22 and instr_20 and rn == 0b1111:
        # Load Halfword literal
        return LdrhLiteralA1
    elif op2 == 0b10 and not instr_22 and not instr_20:
        # Load Dual register
        return LdrdRegisterA1
    elif op2 == 0b10 and not instr_22 and instr_20:
        # Load Signed Byte register
        if not instr_24 and instr_21:
            return LdrsbtA2
        else:
            return LdrsbRegisterA1
    elif op2 == 0b10 and instr_22 and not instr_20 and rn != 0b1111:
        # Load Dual immediate
        return LdrdImmediateA1
    elif op2 == 0b10 and instr_22 and not instr_20 and rn == 0b1111:
        # Load Dual literal
        return LdrdLiteralA1
    elif op2 == 0b10 and instr_22 and instr_20 and rn != 0b1111:
        # Load Signed Byte immediate
        if not instr_24 and instr_21:
            return LdrsbtA1
        else:
            return LdrsbImmediateA1
    elif op2 == 0b10 and instr_22 and instr_20 and rn == 0b1111:
        # Load Signed Byte literal
        return LdrsbLiteralA1
    elif op2 == 0b11 and not instr_22 and not instr_20:
        # Store Dual register
        return StrdRegisterA1
    elif op2 == 0b11 and not instr_22 and instr_20:
        # Load Signed Halfword register
        if not instr_24 and instr_21:
            return LdrshtA2
        else:
            return LdrshRegisterA1
    elif op2 == 0b11 and instr_22 and not instr_20:
        # Store Dual immediate
        return StrdImmediateA1
    elif op2 == 0b11 and instr_22 and instr_20 and rn != 0b1111:
        # Load Signed Halfword immediate
        if not instr_24 and instr_21:
            return LdrshtA1
        else:
            return LdrshImmediateA1
    elif op2 == 0b11 and instr_22 and instr_20 and rn == 0b1111:
        # Load Signed Halfword literal
        return LdrshLiteralA1
