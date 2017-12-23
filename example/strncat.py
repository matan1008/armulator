from bitstring import BitArray
from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_types import RAM
from armulator.armv6.memory_controller_hub import MemoryController

STRNCAT_IMPL = (  # R0 - destination, R1 - source, R2 - num
    "\x10\xb4"  # PUSH {R4}
    "\x43\x1e"  # SUBS R3, R0, #1
    "\x5b\x1c"  # ADDS R3, R3, #1
    "\x1c\x78"  # LDRB R4, [R3]
    "\x00\x2c"  # CMP R4, #0
    "\xfb\xd1"  # BNE 4
    "\x05\xe0"  # B 0x1a
    "\x0c\x78"  # LDRB R4, [R1]
    "\x49\x1c"  # ADDS R1, R1, #1
    "\x1c\x70"  # STRB R4, [R3]
    "\x5b\x1c"  # ADDS R3, R3, #1
    "\x00\x2c"  # CMP R4, #0
    "\x03\xd0"  # BEQ 0x22
    "\x52\x1e"  # SUBS R2, R2, #1
    "\xf7\xd2"  # BCS 0xe
    "\x00\x21"  # MOVS R1, #0
    "\x19\x70"  # STRB R1, [R3]
    "\x10\xbc"  # POP {R4}
    "\x70\x47"  # BX LR
)
FUNCTION_BASE = 0xF0000000


def call_function_without_stack(proc, function_binary, register_params):
    function_memory = RAM(len(function_binary))
    function_memory.write(0, len(function_binary), function_binary)
    mc = MemoryController(function_memory, FUNCTION_BASE, FUNCTION_BASE + len(function_binary))
    proc.mem.memories.append(mc)
    for register_index in register_params:
        proc.registers.set(register_index, register_params[register_index])
    curr_pc = BitArray(hex="0xF0000000")
    proc.registers.branch_to(curr_pc)
    while proc.registers.pc_store_value().uint != 0:
        proc.emulate_cycle()


def strncat(destination, source, num):
    arm = ArmV6("../armulator/armv6/arm_configurations.json")
    arm.take_reset()
    arm.registers.sctlr.set_m(False)
    strings = RAM((len(destination) + len(source)) * 2)
    strings[0, len(destination)] = destination
    source_offset = len(destination) + len(source)
    strings[source_offset, len(source)] = source
    strings_base = 0xE0000000
    mc = MemoryController(strings, strings_base, strings_base + strings.size)
    arm.mem.memories.append(mc)
    call_function_without_stack(arm, STRNCAT_IMPL, {
        0: BitArray(uint=strings_base, length=32),  # Address of destination string
        1: BitArray(uint=strings_base + source_offset, length=32),  # Address of destination string
        2: BitArray(uint=num, length=32)  # Address of destination string
    })
    return strings.read(0, min(len(destination) + len(source) - 1, num))


if __name__ == "__main__":
    assert strncat("hey \x00", "I just met you\x00", 100) == "hey I just met you\x00"
    assert strncat("hey \x00", "I just met you\x00", 8) == "hey I ju"
