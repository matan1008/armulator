from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.shift import shift
from armulator.armv6.bits_ops import add_with_carry
from bitstring import BitArray
from armulator.armv6.arm_exceptions import UndefinedInstructionException


class SubsPcLrArm(AbstractOpcode):
    def __init__(self, register_form, n, opcode_, m=0, shift_t=0, shift_n=0, imm32=0):
        super(SubsPcLrArm, self).__init__()
        self.register_form = register_form
        self.n = n
        self.opcode = opcode_
        self.m = m
        self.shift_t = shift_t
        self.shift_n = shift_n
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_mode_is_hyp():
                raise UndefinedInstructionException()
            elif processor.registers.current_mode_is_user_or_system():
                print "unpredictable"
            else:
                operand2 = shift(processor.registers.get(self.m), self.shift_t, self.shift_n,
                                 processor.registers.cpsr.get_c()) if self.register_form else self.imm32
                if self.opcode == "0000":
                    result = processor.registers.get(self.n) & operand2
                elif self.opcode == "0001":
                    result = processor.registers.get(self.n) ^ operand2
                elif self.opcode == "0010":
                    result = add_with_carry(processor.registers.get(self.n), ~operand2, "1")[0]
                elif self.opcode == "0011":
                    result = add_with_carry(~processor.registers.get(self.n), operand2, "1")[0]
                elif self.opcode == "0100":
                    result = add_with_carry(processor.registers.get(self.n), operand2, "0")[0]
                elif self.opcode == "0101":
                    result = add_with_carry(processor.registers.get(self.n), operand2,
                                            processor.registers.cpsr.get_c())[0]
                elif self.opcode == "0110":
                    result = add_with_carry(processor.registers.get(self.n), ~operand2,
                                            processor.registers.cpsr.get_c())[0]
                elif self.opcode == "0111":
                    result = add_with_carry(~processor.registers.get(self.n), operand2,
                                            processor.registers.cpsr.get_c())[0]
                elif self.opcode == "1100":
                    result = processor.registers.get(self.n) | operand2
                elif self.opcode == "1101":
                    result = operand2
                elif self.opcode == "1110":
                    result = processor.registers.get(self.n) ^ ~operand2
                elif self.opcode == "1111":
                    result = ~operand2
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), BitArray(bin="1111"), True)
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and
                        processor.registers.cpsr.get_t()):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(result)
