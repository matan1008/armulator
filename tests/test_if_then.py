from armulator.arm_v6 import ArmV6
from bitstring import BitArray
from armulator.memory_controller_hub import MemoryController
from armulator.memory_types import RAM


def test_if_then():
    arm = ArmV6()
    arm.take_reset()
    prev_pc = BitArray(hex="0x0F000000")
    arm.registers.sctlr.set_m(False)
    arm.registers.branch_to(prev_pc)
    ram_memory = RAM(0x100)
    ram_memory[0, 2] = "\x0c\xbf"
    ram_memory[2, 2] = "\x41\x1c"
    ram_memory[4, 2] = "\x41\x1e"
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    arm.registers.set(0, BitArray(hex="0x00000012"))
    arm.registers.cpsr.set_n(False)
    arm.registers.cpsr.set_z(True)
    arm.registers.cpsr.set_c(False)
    arm.registers.cpsr.set_v(False)
    arm.emulate_cycle()
    assert arm.registers.cpsr.get_it() == "0x0c"
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000013")
    arm.emulate_cycle()
    assert arm.registers.get(1) == BitArray(hex="0x00000013")
    assert arm.registers.pc_store_value().uint - prev_pc.uint == 6
