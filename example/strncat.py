from bitstring import BitArray
from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_types import RAM
from armulator.armv6.memory_controller_hub import MemoryController

strncat_impl = RAM(38)  # R0 - destination, R1 - source, R2 - num
strncat_impl[0, 2] = "\x10\xb4"  # PUSH {R4}
strncat_impl[2, 2] = "\x43\x1e"  # SUBS R3, R0, #1
strncat_impl[4, 2] = "\x5b\x1c"  # ADDS R3, R3, #1
strncat_impl[6, 2] = "\x1c\x78"  # LDRB R4, [R3]
strncat_impl[8, 2] = "\x00\x2c"  # CMP R4, #0
strncat_impl[0xa, 2] = "\xfb\xd1"  # BNE 4
strncat_impl[0xc, 2] = "\x05\xe0"  # B 0x1a
strncat_impl[0xe, 2] = "\x0c\x78"  # LDRB R4, [R1]
strncat_impl[0x10, 2] = "\x49\x1c"  # ADDS R1, R1, #1
strncat_impl[0x12, 2] = "\x1c\x70"  # STRB R4, [R3]
strncat_impl[0x14, 2] = "\x5b\x1c"  # ADDS R3, R3, #1
strncat_impl[0x16, 2] = "\x00\x2c"  # CMP R4, #0
strncat_impl[0x18, 2] = "\x03\xd0"  # BEQ 0x22
strncat_impl[0x1a, 2] = "\x52\x1e"  # SUBS R2, R2, #1
strncat_impl[0x1c, 2] = "\xf7\xd2"  # BCS 0xe
strncat_impl[0x1e, 2] = "\x00\x21"  # MOVS R1, #0
strncat_impl[0x20, 2] = "\x19\x70"  # STRB R1, [R3]
strncat_impl[0x22, 2] = "\x10\xbc"  # POP {R4}
strncat_impl[0x24, 2] = "\x70\x47"  # BX LR


def strncat(destination, source, num):
    arm = ArmV6()
    arm.take_reset()
    curr_pc = BitArray(hex="0xF0000000")
    arm.registers.sctlr.set_m(False)
    mc = MemoryController(strncat_impl, 0xF0000000, 0xF0000026)
    arm.mem.memories.append(mc)
    strings = RAM((len(destination) + len(source)) * 2)
    strings[0, len(destination)] = destination
    strings[len(destination) + len(source), len(source)] = source
    strings_base = 0xE0000000
    mc = MemoryController(strings, strings_base, strings_base + (len(destination) + len(source)) * 2)
    arm.mem.memories.append(mc)
    arm.registers.set(0, BitArray(uint=strings_base, length=32))
    arm.registers.set(1, BitArray(uint=strings_base + len(destination) + len(source), length=32))
    arm.registers.set(2, BitArray(uint=num, length=32))
    arm.registers.branch_to(curr_pc)
    while arm.registers.pc_store_value().uint != 0:
        arm.emulate_cycle()
    return strings.read(0, min(len(destination) + len(source), num))


print strncat("hey \x00", "I just met you\x00", 8)
print strncat("hey \x00", "I just met you\x00", 100)
