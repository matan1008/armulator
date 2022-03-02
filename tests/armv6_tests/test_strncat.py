import pytest

from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_controller_hub import MemoryController
from armulator.armv6.memory_types import RAM

STRNCAT_IMPL = (  # R0 - destination, R1 - source, R2 - num
    b"\x10\xb4"  # PUSH {R4}
    b"\x43\x1e"  # SUBS R3, R0, #1
    b"\x5b\x1c"  # ADDS R3, R3, #1
    b"\x1c\x78"  # LDRB R4, [R3]
    b"\x00\x2c"  # CMP R4, #0
    b"\xfb\xd1"  # BNE 4
    b"\x05\xe0"  # B 0x1a
    b"\x0c\x78"  # LDRB R4, [R1]
    b"\x49\x1c"  # ADDS R1, R1, #1
    b"\x1c\x70"  # STRB R4, [R3]
    b"\x5b\x1c"  # ADDS R3, R3, #1
    b"\x00\x2c"  # CMP R4, #0
    b"\x03\xd0"  # BEQ 0x22
    b"\x52\x1e"  # SUBS R2, R2, #1
    b"\xf7\xd2"  # BCS 0xe
    b"\x00\x21"  # MOVS R1, #0
    b"\x19\x70"  # STRB R1, [R3]
    b"\x10\xbc"  # POP {R4}
    b"\x70\x47"  # BX LR
)
FUNCTION_BASE = 0xF0000000


def call_function_without_stack(proc, function_binary, register_params):
    function_memory = RAM(len(function_binary))
    function_memory.write(0, len(function_binary), function_binary)
    mc = MemoryController(function_memory, FUNCTION_BASE, FUNCTION_BASE + len(function_binary))
    proc.mem.memories.append(mc)
    for register_index in register_params:
        proc.registers.set(register_index, register_params[register_index])
    curr_pc = 0xF0000000
    proc.registers.branch_to(curr_pc)
    while proc.registers.pc_store_value() != 0:
        proc.emulate_cycle()


def strncat(destination, source, num):
    arm = ArmV6()
    arm.take_reset()
    arm.registers.sctlr.m = 0
    strings = RAM((len(destination) + len(source)) * 2)
    strings[0, len(destination)] = destination
    source_offset = len(destination) + len(source)
    strings[source_offset, len(source)] = source
    strings_base = 0xE0000000
    mc = MemoryController(strings, strings_base, strings_base + strings.size)
    arm.mem.memories.append(mc)
    call_function_without_stack(arm, STRNCAT_IMPL, {
        0: strings_base,  # Address of destination string
        1: strings_base + source_offset,  # Address of destination string
        2: num,  # Address of destination string
    })
    return strings.read(0, min(len(destination) + len(source) - 1, num))


@pytest.mark.parametrize('str1, str2, length, result', [
    (b'hey \x00', b'I just met you\x00', 100, b'hey I just met you\x00'),
    (b'hey \x00', b'I just met you\x00', 8, b'hey I ju')
])
def test_strncat(str1, str2, length, result):
    assert strncat(str1, str2, length) == result
