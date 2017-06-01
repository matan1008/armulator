from armulator.arm_v6 import ArmV6
from bitstring import BitArray
from armulator.shift import SRType
from armulator.memory_types import RAM
from armulator.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit. \
    thumb_load_store_single_data_item.ldr_register_thumb_t1 import LdrRegisterThumbT1


def test_ldr_register_thumb():
    arm = ArmV6()
    arm.take_reset()
    instr = BitArray(bin="0101100001010011")
    # setting Data Region registers
    arm.registers.drsrs[0].set_en(True)  # enabling memory region
    arm.registers.drsrs[0].set_rsize("0b00010")  # setting region size
    arm.registers.drbars[0] = BitArray(hex="0x0F000000")  # setting region base address
    arm.registers.dracrs[0].set_ap("0b011")  # setting access permissions
    arm.registers.mpuir.set_iregion("0x01")  # declaring the region
    arm.registers.mpuir.set_dregion("0x01")  # declaring the region
    ram_memory = RAM(0x100)
    ram_memory.write(0x4, 4, "ECIN")
    arm.mem.memories.append((ram_memory, (0x0F000000, 0x0F000100)))
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == LdrRegisterThumbT1
    assert opcode.m == 1
    assert opcode.n == 2
    assert opcode.t == 3
    assert opcode.shift_n == 0
    assert opcode.shift_t == SRType.SRType_LSL
    arm.registers.set(opcode.n, BitArray(hex="0x0F000004"))
    arm.execute_instruction(opcode)
    assert arm.registers.get(opcode.t).bytes == "NICE"
