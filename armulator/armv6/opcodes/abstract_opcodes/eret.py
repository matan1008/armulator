from armulator.armv6.opcodes.opcode import Opcode

from armulator.armv6.enums import InstrSet


class Eret(Opcode):
    def __init__(self, instruction):
        super().__init__(instruction)

    def execute(self, processor):
        if processor.condition_passed():
            if (processor.registers.current_mode_is_user_or_system() or
                    processor.registers.current_instr_set() == InstrSet.THUMB_EE):
                print('unpredictable')
            else:
                new_pc_value = (processor.registers.elr_hyp
                                if processor.registers.current_mode_is_hyp()
                                else processor.registers.get(14))
                processor.registers.cpsr_write_by_instr(processor.registers.get_spsr(), 0b1111, True)
                if (processor.registers.cpsr.m == 0b11010 and
                        processor.registers.cpsr.j and
                        processor.registers.cpsr.t):
                    print('unpredictable')
                else:
                    processor.branch_write_pc(new_pc_value)
