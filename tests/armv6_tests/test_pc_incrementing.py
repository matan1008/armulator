from armulator.armv6.arm_v6 import ArmV6
from bitstring import BitArray
from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM


def test_increment_pc():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = BitArray(hex="0x0F000000")
    arm.registers.sctlr.set_m(False)
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0, 2] = b"\x41\x1c"
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.registers.set(0, BitArray(hex="0x00000012"))
    arm.emulate_cycle()
    assert not arm.registers.cpsr.get_n()
    assert not arm.registers.cpsr.get_z()
    assert not arm.registers.cpsr.get_c()
    assert not arm.registers.cpsr.get_v()
    assert arm.registers.pc_store_value().uint - prev_pc.uint == 2
    assert arm.registers.get(1) == BitArray(hex="0x00000013")


def test_branching_t1():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = BitArray(hex="0x000514F6")
    arm.registers.sctlr.set_m(False)
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0xd8, 2] = b"\x41\x1c"  # ADDS R1, R0, #1
    ram_memory[0xf6, 2] = b"\xef\xdc"
    mc = MemoryController(ram_memory, 0x00051400, 0x00051500)
    arm.mem.memories.append(mc)
    arm.registers.set(0, BitArray(hex="0x00000012"))
    arm.registers.cpsr.set_n(False)
    arm.registers.cpsr.set_z(False)
    arm.registers.cpsr.set_c(False)
    arm.registers.cpsr.set_v(False)
    arm.emulate_cycle()
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000013")
