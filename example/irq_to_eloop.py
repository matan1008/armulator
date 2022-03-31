import time
from threading import Thread

from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_types import RAM
from armulator.armv6.memory_controller_hub import MemoryController

ELOOP = b"\xfe\xe7"
ADDR = 0x1000


class EmuRunner(Thread):
    def __init__(self, emu):
        Thread.__init__(self)
        self.emu = emu
        self.stop_called = False

    def run(self):
        while not self.stop_called:
            time.sleep(1)
            self.emu.emulate_cycle()
            print(self.emu.registers.pc_store_value())

    def stop(self):
        self.stop_called = True


def prepare_emulator():
    arm = ArmV6()
    arm.registers.sctlr.m = 0
    # Add eloop in the IRQ vector
    arm.mem.memories[0].mem.write(0x18, len(ELOOP), ELOOP)
    # Add eloop in the desired addr
    mem = RAM(len(ELOOP))
    mem.write(0, len(ELOOP), ELOOP)
    mc = MemoryController(mem, ADDR, ADDR + len(ELOOP))
    arm.mem.memories.append(mc)
    # Reboot with new settings
    arm.take_reset()
    # Jump to the eloop
    arm.registers.branch_to(ADDR)
    return arm


def main():
    arm = prepare_emulator()
    runner = EmuRunner(arm)
    runner.start()
    time.sleep(5)
    # Assert that the eloop works
    assert arm.registers.pc_store_value() == ADDR
    # Send IRQ exception
    print("Sending IRQ")
    arm.registers.take_physical_irq_exception()
    print("IRQ sent")
    # Assert jumping to IRQ vector and changing mode
    assert arm.registers.pc_store_value() == 0x18
    assert arm.registers.cpsr.m == 0b10010

    runner.stop()
    runner.join()


if __name__ == '__main__':
    main()
