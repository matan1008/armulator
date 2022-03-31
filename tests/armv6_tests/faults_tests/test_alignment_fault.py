import pytest
from armulator.armv6.arm_v6 import ArmV6
from armulator.armv6.memory_controller_hub import MemoryController

from armulator.armv6.memory_types import RAM
from armulator.armv6.opcodes.concrete.ldm_thumb_t1 import LdmThumbT1
from armulator.armv6.arm_exceptions import DataAbortException


def test_ldm_alignment_fault():
    arm = ArmV6()
    arm.take_reset()
    instr = 0b1100100100100110
    arm.opcode_len = 16
    arm.registers.drsrs[0].en = 1  # enabling memory region
    arm.registers.drsrs[0].rsize = 0b01000  # setting region size
    arm.registers.drbars[0] = 0x0F000000  # setting region base address
    arm.registers.dracrs[0].ap = 0b011  # setting access permissions
    arm.registers.mpuir.iregion = 0x01  # declaring the region
    arm.registers.mpuir.dregion = 0x01  # declaring the region
    arm.registers.sctlr.u = 1
    ram_memory = RAM(0x100)
    mc = MemoryController(ram_memory, 0x0F000000, 0x0F000100)
    arm.mem.memories.append(mc)
    opcode = arm.decode_instruction(instr)
    opcode = opcode.from_bitarray(instr, arm)
    assert type(opcode) == LdmThumbT1
    assert opcode.wback is False
    assert opcode.n == 1
    assert opcode.registers == 0b0000000000100110
    arm.registers.set(opcode.n, 0x0F000003)
    with pytest.raises(DataAbortException) as dabort_exception:
        arm.execute_instruction(opcode)
    assert dabort_exception.value.is_alignment_fault()
    assert not dabort_exception.value.second_stage_abort()
    arm.registers.take_data_abort_exception(dabort_exception.value)
    assert arm.registers.get_pc() == 0x00000014
