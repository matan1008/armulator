from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.enums import InstrSet


class Eret(AbstractOpcode):
    def __init__(self):
        super(Eret, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.registers.current_mode_is_user_or_system() or
                    processor.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print "unpredictable"
            else:
                new_pc_value = (processor.registers.elr_hyp
                                if processor.registers.current_mode_is_hyp()
                                else processor.registers.get(14))
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), BitArray(bin="1111"), True)
                if (processor.registers.cpsr.get_m() == "0b11010" and
                        processor.registers.cpsr.get_j() and
                        processor.registers.cpsr.get_t()):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(new_pc_value)
