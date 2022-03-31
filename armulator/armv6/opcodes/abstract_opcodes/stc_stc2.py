from armulator.armv6.arm_exceptions import EndOfInstruction
from armulator.armv6.bits_ops import add as bits_add, sub as bits_sub
from armulator.armv6.opcodes.opcode import Opcode


class StcStc2(Opcode):
    def __init__(self, instruction, cp, n, add, imm32, index, wback):
        super().__init__(instruction)
        self.cp = cp
        self.n = n
        self.add = add
        self.imm32 = imm32
        self.index = index
        self.wback = wback

    def execute(self, processor):
        if processor.condition_passed():
            if not processor.coproc_accepted(self.cp, processor.this_instr()):
                processor.generate_coprocessor_exception()
            else:
                try:
                    processor.null_check_if_thumbee(self.n)
                except EndOfInstruction:
                    pass
                else:
                    offset_addr = bits_add(processor.registers.get(self.n), self.imm32, 32) if self.add else bits_sub(
                        processor.registers.get(self.n), self.imm32, 32)
                    address = offset_addr if self.index else processor.registers.get(self.n)
                    first_pass = True
                    while first_pass or processor.coproc_done_storing(self.cp, processor.this_instr()):
                        first_pass = False
                        processor.mem_a_set(address, 4,
                                            processor.coproc_get_word_to_store(self.cp, processor.this_instr()))
                        address = bits_add(address, 4, 32)
                    if self.wback:
                        processor.registers.set(self.n, offset_addr)
