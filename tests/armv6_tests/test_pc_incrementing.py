from armulator.armv6.arm_v6 import ArmV6

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM


def test_increment_pc():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = 0x0F000000
    arm.registers.sctlr.m = 0
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0, 2] = b'\x41\x1c'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.registers.set(0, 0x00000012)
    arm.emulate_cycle()
    assert not arm.registers.cpsr.n
    assert not arm.registers.cpsr.z
    assert not arm.registers.cpsr.c
    assert not arm.registers.cpsr.v
    assert arm.registers.pc_store_value() - prev_pc == 2
    assert arm.registers.get(1) == 0x00000013
