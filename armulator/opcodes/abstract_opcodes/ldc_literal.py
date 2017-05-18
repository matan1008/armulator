from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import EndOfInstruction
from armulator.bits_ops import add as bits_add, sub as bits_sub, align
from bitstring import BitArray


class LdcLiteral(AbstractOpcode):
    def __init__(self, cp, add, imm32, index):
        super(LdcLiteral, self).__init__()
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
                    offset_addr = bits_add(align(processor.core_registers.get_pc(), 4), self.imm32,
                                           32) if self.add else bits_sub(align(processor.core_registers.get_pc(), 4),
                                                                         self.imm32, 32)
                    address = offset_addr if self.index else align(processor.core_registers.get_pc(), 4)
                    first_pass = True
                    while first_pass or processor.coproc_done_loading(self.cp, processor.this_instr()):
                        first_pass = False
                        processor.coproc_send_loaded_word(processor.mem_a_get(address, 4), self.cp,
                                                          processor.this_instr())
                        address = bits_add(address, BitArray(bin="100"), 32)
