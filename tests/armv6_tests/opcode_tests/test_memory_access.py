from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_controller_hub import MemoryController
from bitstring import BitArray
from armulator.armv6.shift import SRType
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit. \
    thumb_load_store_single_data_item.ldr_register_thumb_t1 import LdrRegisterThumbT1
from armulator.armv6.opcodes.thumb_instruction_set.thumb_instruction_set_encoding_16_bit.stm_t1 import StmT1


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
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
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


def test_stm_thumb():
    arm = ArmV6()
    arm.take_reset()
    instr = BitArray(bin="1100000100100100")
    arm.registers.drsrs[0].set_en(True)  # enabling memory region
    arm.registers.drsrs[0].set_rsize("0b01000")  # setting region size
    arm.registers.drbars[0] = BitArray(hex="0x0F000000")  # setting region base address
    arm.registers.dracrs[0].set_ap("0b011")  # setting access permissions
    arm.registers.mpuir.set_iregion("0x01")  # declaring the region
    arm.registers.mpuir.set_dregion("0x01")  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == StmT1
    assert opcode.wback is True
    assert opcode.n == 1
    assert opcode.registers == "0b0000000000100100"
    arm.registers.set(opcode.n, BitArray(hex="0x0F000004"))
    arm.registers.set(2, BitArray(bytes="YREV"))
    arm.registers.set(5, BitArray(bytes="ECIN"))
    arm.execute_instruction(opcode)
    assert ram_memory[4, 8] == "VERYNICE"
    assert arm.registers.get(opcode.n) == "0x0F00000C"
