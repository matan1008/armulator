from armulator.opcodes.abstract_opcode import AbstractOpcode
from bitstring import BitArray
from armulator.enums import InstrSet


class Eret(AbstractOpcode):
    def __init__(self):
        super(Eret, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.core_registers.current_mode_is_user_or_system() or
                    processor.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE):
                print "unpredictable"
            else:
                new_pc_value = (processor.core_registers.ELR_hyp
                                if processor.core_registers.current_mode_is_hyp()
                                else processor.core_registers.get(14))
                processor.core_registers.cpsr_write_by_instr(processor.core_registers.get_spsr(), BitArray(bin="1111"),
                                                             True)
                if (processor.core_registers.cpsr.get_m() == "0b11010" and
                        processor.core_registers.cpsr.get_j() and
                        processor.core_registers.cpsr.get_t()):
                    print "unpredictable"
                else:
                    processor.branch_write_pc(new_pc_value)
