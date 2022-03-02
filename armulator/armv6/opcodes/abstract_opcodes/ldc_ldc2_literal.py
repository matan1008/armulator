from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub, align
from armulator.armv6.opcodes.opcode import Opcode


class LdcLdc2Literal(Opcode):
    def __init__(self, instruction, cp, add, imm32, index):
        super().__init__(instruction)
        self.cp = cp
        self.add = add
        self.imm32 = imm32
        self.index = index

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                try:
                    processor.null_check_if_thumbee(15)
                except EndOfInstruction:
                    pass
                else:
                    offset_addr = bits_add(align(processor.registers.get_pc(), 4), self.imm32,
                                           32) if self.add else bits_sub(align(processor.registers.get_pc(), 4),
                                                                         self.imm32, 32)
                    address = offset_addr if self.index else align(processor.registers.get_pc(), 4)
                    first_pass = True
                    while first_pass or processor.coproc_done_loading(self.cp, processor.this_instr()):
                        first_pass = False
                        processor.coproc_send_loaded_word(processor.mem_a_get(address, 4), self.cp,
                                                          processor.this_instr())
                        address = bits_add(address, 4, 32)
