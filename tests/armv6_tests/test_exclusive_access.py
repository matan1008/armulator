from armulator.armv6.arm_v6 import ArmV6
from bitstring import BitArray
from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM


def test_exclusive_sanity():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = BitArray(hex="0x0F000000")
    arm.registers.sctlr.set_m(False)
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0, 2] = "\x40\x20"  # MOVS R0, 0x40
    ram_memory[2, 2] = "\x01\x21"  # MOVS R1, 0x1
    ram_memory[4, 2] = "\x01\x60"  # STR R1, [R0]
    ram_memory[6, 2] = "\x00\x21"  # MOVS R1, 0x0
    ram_memory[8, 4] = "\x50\xe8\x00\x1f"  # LDREX R1, [R0]
    ram_memory[12, 4] = "\x50\xe8\x00\x2f"  # LDREX R2, [R0]
    ram_memory[16, 2] = "\x01\x31"  # ADDS R1, 0x1
    ram_memory[18, 2] = "\x02\x32"  # ADDS R2, 0x2
    ram_memory[20, 4] = "\x40\xe8\x00\x13"  # STREX R3, R1, [R0]
    ram_memory[24, 4] = "\x40\xe8\x00\x23"  # STREX R3, R2, [R0]
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.registers.cpsr.set_n(False)
    arm.registers.cpsr.set_z(False)
    arm.registers.cpsr.set_c(False)
    arm.registers.cpsr.set_v(False)
    arm.emulate_cycle()
    assert arm.registers.get(0) == BitArray(hex="0x00000040")
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000001")
    arm.emulate_cycle()
    assert arm.mem.memories[0].mem[64, 4] == "\x01\x00\x00\x00"
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000000")
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000001")
    arm.emulate_cycle()
    assert arm.registers.get(2) == BitArray(hex="0x00000001")
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000002")
    arm.emulate_cycle()
    assert arm.registers.get(2) == BitArray(hex="0x00000003")
    arm.emulate_cycle()
    assert arm.registers.get(3) == BitArray(hex="0x00000000")
    assert arm.mem.memories[0].mem[64, 4] == "\x02\x00\x00\x00"
    arm.emulate_cycle()
    assert arm.registers.get(3) == BitArray(hex="0x00000001")
    assert arm.mem.memories[0].mem[64, 4] == "\x02\x00\x00\x00"
