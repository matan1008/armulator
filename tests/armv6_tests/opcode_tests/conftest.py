import pytest
from armulator.armv6.arm_v6 import ArmV6


class ArmV6WithoutFetch(ArmV6):
    def fetch_instruction(self):
        return self.opcode


@pytest.fixture
def thumb_v6_without_fetch():
    proc = ArmV6WithoutFetch()
    proc.take_reset()
    return proc


@pytest.fixture
def arm_v6_without_fetch():
    proc = ArmV6WithoutFetch()
    proc.registers.sctlr.te = 0
    proc.take_reset()
    return proc
