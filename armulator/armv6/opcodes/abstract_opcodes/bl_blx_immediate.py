from armulator.armv6.bits_ops import add, sub, align
from armulator.armv6.enums import InstrSet
from armulator.armv6.opcodes.opcode import Opcode


class BlBlxImmediate(Opcode):
    def __init__(self, instruction, target_instr_set, imm32):
        super().__init__(instruction)
        self.target_instr_set = target_instr_set
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_instr_set() == InstrSet.ARM:
                processor.registers.set_lr(sub(processor.registers.get_pc(), 4, 32))
            else:
                processor.registers.set_lr(processor.registers.get_pc() | 0b1)
            if self.target_instr_set == InstrSet.ARM:
                target_address = add(align(processor.registers.get_pc(), 4), self.imm32, 32)
            else:
                target_address = add(processor.registers.get_pc(), self.imm32, 32)
            processor.registers.select_instr_set(self.target_instr_set)
            processor.branch_write_pc(target_address)
