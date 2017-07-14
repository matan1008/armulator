from armulator.armv6.opcodes.abstract_opcode import AbstractOpcode
from armulator.armv6.bits_ops import add, sub, align
from armulator.armv6.enums import InstrSet
from bitstring import BitArray


class BlImmediate(AbstractOpcode):
    def __init__(self, target_instr_set, imm32):
        super(BlImmediate, self).__init__()
        self.target_instr_set = target_instr_set
        self.imm32 = imm32

    def execute(self, processor):
        if processor.condition_passed():
            if processor.registers.current_instr_set() == InstrSet.InstrSet_ARM:
                processor.registers.set_lr(sub(processor.registers.get_pc(), BitArray(bin="100"), 32))
            else:
                processor.registers.set_lr(processor.registers.get_pc()[0:31] + "0b1")
            if self.target_instr_set == InstrSet.InstrSet_ARM:
                target_address = add(align(processor.registers.get_pc(), 4), self.imm32, 32)
            else:
                target_address = add(processor.registers.get_pc(), self.imm32, 32)
            processor.registers.select_instr_set(self.target_instr_set)
            processor.branch_write_pc(target_address)
