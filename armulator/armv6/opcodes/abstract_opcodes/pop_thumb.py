from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add, bit_at, substring, bit_count
from armulator.armv6.opcodes.opcode import Opcode


class PopThumb(Opcode):
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
                address = processor.registers.get_sp()
                for i in range(15):
                    if bit_at(self.registers, i):
                        processor.registers.set(
                            i,
                            (processor.mem_u_get(address, 4) if self.unaligned_allowed else processor.mem_a_get(address,
                                                                                                                4))
                        )
                        address = add(address, 4, 32)
                if bit_at(self.registers, 15):
                    if self.unaligned_allowed:
                        if substring(address, 1, 0) == 0b00:
                            processor.load_write_pc(processor.mem_u_get(address, 4))
                        else:
                            print('unpredictable')
                    else:
                        processor.load_write_pc(processor.mem_a_get(address, 4))
                if not bit_at(self.registers, 13):
                    processor.registers.set_sp(add(
                        processor.registers.get_sp(), 4 * bit_count(self.registers, 1, 16), 32
                    ))
                if bit_at(self.registers, 13):
                    processor.registers.set_sp(0x00000000)  # unknown
