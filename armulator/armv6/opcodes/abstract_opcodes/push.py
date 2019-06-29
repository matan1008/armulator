from builtins import range
from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add, sub, lowest_set_bit_ref
from bitstring import BitArray
from armulator.armv6.arm_exceptions import EndOfInstruction


class Push(AbstractOpcode):
    def __init__(self, registers, unaligned_allowed):
        super(Push, self).__init__()
        self.registers = registers
        self.unaligned_allowed = unaligned_allowed

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(13)
            except EndOfInstruction:
                pass
            else:
                address = sub(processor.registers.get_sp(),
                              BitArray(uint=(4 * self.registers.count(1)), length=32), 32)
                for i in range(15):
                    if self.registers[15 - i]:
                        if i == 13 and i != lowest_set_bit_ref(self.registers):
                            processor.mem_a_set(address, 4, BitArray(length=32))  # unknown
                        else:
                            if self.unaligned_allowed:
                                processor.mem_u_set(address, 4, processor.registers.get(i))
                            else:
                                processor.mem_a_set(address, 4, processor.registers.get(i))
                        address = add(address, BitArray(bin="100"), 32)
                if self.registers[0]:
                    if self.unaligned_allowed:
                        processor.mem_u_set(address, 4, processor.registers.pc_store_value())
                    else:
                        processor.mem_a_set(address, 4, processor.registers.pc_store_value())
                processor.registers.set_sp(
                        sub(processor.registers.get_sp(), BitArray(uint=(4 * self.registers.count(1)), length=32),
                            32))
