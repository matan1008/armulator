from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add, sub, lowest_set_bit_ref, bit_count, bit_at
from armulator.armv6.opcodes.opcode import Opcode


class Push(Opcode):
    def __init__(self, instruction, registers, unaligned_allowed):
        super().__init__(instruction)
        self.registers = registers
        self.unaligned_allowed = unaligned_allowed

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(13)
            except EndOfInstruction:
                pass
            else:
                address = sub(processor.registers.get_sp(), 4 * bit_count(self.registers, 1, 32), 32)
                for i in range(15):
                    if bit_at(self.registers, i):
                        if i == 13 and i != lowest_set_bit_ref(self.registers):
                            processor.mem_a_set(address, 4, 0x00000000)  # unknown
                        else:
                            if self.unaligned_allowed:
                                processor.mem_u_set(address, 4, processor.registers.get(i))
                            else:
                                processor.mem_a_set(address, 4, processor.registers.get(i))
                        address = add(address, 4, 32)
                if bit_at(self.registers, 15):
                    if self.unaligned_allowed:
                        processor.mem_u_set(address, 4, processor.registers.pc_store_value())
                    else:
                        processor.mem_a_set(address, 4, processor.registers.pc_store_value())
                processor.registers.set_sp(sub(
                    processor.registers.get_sp(), 4 * bit_count(self.registers, 1, 32), 32
                ))
