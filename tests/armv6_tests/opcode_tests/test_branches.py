from armulator.armv6.arm_v6 import ArmV6
from bitstring import BitArray
from armulator.armv6.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit. \
    thumb_conditional_branch_and_supervisor_call.b_t1 import BT1


def test_conditional_branch_thumb():
    arm = ArmV6()
    arm.take_reset()
    instr = BitArray(bin="1101000000000100")
    prev_pc = BitArray(hex="0x0F000000")
    arm.registers.branch_to(prev_pc)
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == BT1
    assert opcode.imm32 == BitArray(hex="0x00000008")
    assert opcode.instruction == instr
    arm.registers.cpsr.set_n(False)
    arm.registers.cpsr.set_z(True)
    arm.registers.cpsr.set_c(False)
    arm.registers.cpsr.set_v(False)
    arm.execute_instruction(opcode)
    assert arm.registers.pc_store_value() == "0x0F00000C"
