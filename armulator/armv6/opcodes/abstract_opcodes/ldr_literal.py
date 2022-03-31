from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align, lower_chunk, chain
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import ror


class LdrLiteral(Opcode):
    def __init__(self, instruction, add, imm32, t):
        super().__init__(instruction)
        self.add = add
        self.imm32 = imm32
        self.t = t

    def execute(self, processor):
        if processor.condition_passed():
            try:
                processor.null_check_if_thumbee(15)
            except EndOfInstruction:
                pass
            else:
                base = align(processor.registers.get_pc(), 4)
                address = bits_add(base, self.imm32, 32) if self.add else bits_sub(base, self.imm32, 32)
                data = processor.mem_u_get(address, 4)
                if self.t == 15:
                    if lower_chunk(address, 2) == 0b00:
                        processor.load_write_pc(data)
                    else:
                        print('unpredictable')
                elif processor.unaligned_support() or lower_chunk(address, 2) == 0b00:
                    processor.registers.set(self.t, data)
                else:
                    if processor.registers.current_instr_set() == InstrSet.ARM:
                        processor.registers.set(self.t, ror(data, 32, 8 * lower_chunk(address, 2)))
                    else:
                        processor.registers.set(self.t, 0x00000000)  # unknown

    def instruction_syndrome(self):
        if self.t == 15:
            return 0b000000000
        else:
            return chain(0b11000, self.t, 4)
