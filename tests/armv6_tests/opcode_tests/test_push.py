import struct

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.push_a1 import PushA1
from armulator.armv6.opcodes.concrete.push_a2 import PushA2
from armulator.armv6.opcodes.concrete.push_t1 import PushT1
from armulator.armv6.opcodes.concrete.push_t2 import PushT2
from armulator.armv6.opcodes.concrete.push_t3 import PushT3


def test_push_t1(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b1011010100000001
    arm.opcode_len = 16
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PushT1)
    assert opcode.registers == 0b0100000000000001
    assert not opcode.unaligned_allowed
    arm.registers.set(0, struct.unpack('>I', b'YREV')[0])
    arm.registers.set_sp(0x0F000008)
    arm.registers.set_lr(struct.unpack('>I', b'ECIN')[0])
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'VERYNICE'
    assert arm.registers.get_sp() == 0x0F000000


def test_push_t2(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11101001001011010100000000000001
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PushT2)
    assert opcode.registers == 0b0100000000000001
    assert opcode.unaligned_allowed
    arm.registers.set(0, struct.unpack('>I', b'YREV')[0])
    arm.registers.set_sp(0x0F000008)
    arm.registers.set_lr(struct.unpack('>I', b'ECIN')[0])
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'VERYNICE'
    assert arm.registers.get_sp() == 0x0F000000


def test_push_t3(thumb_v6_without_fetch):
    arm = thumb_v6_without_fetch
    arm.opcode = 0b11111000010011010000110100000100
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PushT3)
    assert opcode.registers == 0b0000000000000001
    assert opcode.unaligned_allowed
    arm.registers.set(0, 0x11223344)
    arm.registers.set_sp(0x0F000004)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x33\x22\x11'
    assert arm.registers.get_sp() == 0x0F000000


def test_push_a2(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11100101001011010000000000000100
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PushA2)
    assert opcode.registers == 0b0000000000000001
    assert opcode.unaligned_allowed
    arm.registers.set(0, 0x11223344)
    arm.registers.set_sp(0x0F000004)
    arm.emulate_cycle()
    assert ram_memory[0, 4] == b'\x44\x33\x22\x11'
    assert arm.registers.get_sp() == 0x0F000000


def test_push_a1(arm_v6_without_fetch):
    arm = arm_v6_without_fetch
    arm.opcode = 0b11101001001011010100000000000001
    arm.opcode_len = 32
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(arm.opcode)
    opcode = opcode.from_bitarray(arm.opcode, arm)
    assert isinstance(opcode, PushA1)
    assert opcode.registers == 0b0100000000000001
    assert not opcode.unaligned_allowed
    arm.registers.set(0, 0x11223344)
    arm.registers.set_sp(0x0F000008)
    arm.registers.set_lr(0x55667788)
    arm.emulate_cycle()
    assert ram_memory[0, 8] == b'\x44\x33\x22\x11\x88\x77\x66\x55'
    assert arm.registers.get_sp() == 0x0F000000
