from armulator.armv6.arm_exceptions import UndefinedInstructionException
from armulator.armv6.bits_ops import add_with_carry, bit_not
from armulator.armv6.opcodes.opcode import Opcode
from armulator.armv6.shift import shift, SRType


class SubsPcLrArm(Opcode):
    def __init__(self, instruction, register_form, n, opcode, m=0, shift_t=SRType.LSL, shift_n=0, imm32=0):
        super().__init__(instruction)
        self.register_form = register_form
        self.n = n
        self.opcode = opcode
        self.m = m
        self.shift_t = shift_t
        self.shift_n = shift_n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print('unpredictable')
            else:
                operand2 = shift(processor.registers.get(self.m), 32, self.shift_t, self.shift_n,
                                 processor.registers.cpsr.c) if self.register_form else self.imm32
                if self.opcode == 0b0000:
                    result = processor.registers.get(self.n) & operand2
                elif self.opcode == 0b0001:
                    result = processor.registers.get(self.n) ^ operand2
                elif self.opcode == 0b0010:
                    result = add_with_carry(processor.registers.get(self.n), bit_not(operand2, 32), 1)[0]
                elif self.opcode == 0b0011:
                    result = add_with_carry(bit_not(processor.registers.get(self.n), 32), operand2, 1)[0]
                elif self.opcode == 0b0100:
                    result = add_with_carry(processor.registers.get(self.n), operand2, 0)[0]
                elif self.opcode == 0b0101:
                    result = add_with_carry(processor.registers.get(self.n), operand2, processor.registers.cpsr.c)[0]
                elif self.opcode == 0b0110:
                    result = add_with_carry(processor.registers.get(self.n), bit_not(operand2, 32),
                                            processor.registers.cpsr.c)[0]
                elif self.opcode == 0b0111:
                    result = add_with_carry(bit_not(processor.registers.get(self.n), 32), operand2,
                                            processor.registers.cpsr.c)[0]
                elif self.opcode == 0b1100:
                    result = processor.registers.get(self.n) | operand2
                elif self.opcode == 0b1101:
                    result = operand2
                elif self.opcode == 0b1110:
                    result = processor.registers.get(self.n) & bit_not(operand2, 32)
                elif self.opcode == 0b1111:
                    result = bit_not(operand2, 32)
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), 0b1111, True)
                if processor.registers.cpsr.m == 0b11010 and processor.registers.cpsr.j and processor.registers.cpsr.t:
                    print('unpredictable')
                else:
                    processor.branch_write_pc(result)
