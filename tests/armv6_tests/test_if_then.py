from armulator.armv6.arm_v6 import ArmV6

from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM


def test_if_then():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = 0x0F000000
    arm.registers.sctlr.m = 0
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0, 2] = b'\x0c\xbf'
    ram_memory[2, 2] = b'\x41\x1c'
    ram_memory[4, 2] = b'\x41\x1e'
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.registers.set(0, 0x00000012)
    arm.registers.cpsr.n = 0
    arm.registers.cpsr.z = 1
    arm.registers.cpsr.c = 0
    arm.registers.cpsr.v = 0
    arm.emulate_cycle()
    assert arm.registers.cpsr.it == 0x0c
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0x00000013
    arm.emulate_cycle()
    assert arm.registers.get(1) == 0x00000013
    assert arm.registers.pc_store_value() - prev_pc == 6
