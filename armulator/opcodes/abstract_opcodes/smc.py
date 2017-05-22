from armulator.opcodes.abstract_opcode import AbstractOpcode
from armulator.arm_exceptions import SMCException, UndefinedInstructionException
from bitstring import BitArray
from armulator.configurations import HaveSecurityExt, HaveVirtExt


class Smc(AbstractOpcode):
    def __init__(self):
        super(Smc, self).__init__()

    def execute(self, processor):
        if processor.condition_passed():
            if HaveSecurityExt() and processor.core_registers.current_mode_is_not_user():
                if (HaveVirtExt() and not processor.core_registers.is_secure() and
                        not processor.core_registers.current_mode_is_hyp() and
                        processor.core_registers.get_hcr_tsc() == "1"):
                    hsr_string = BitArray(25)
                    processor.write_hsr("010011", hsr_string)
                    processor.core_registers.take_hyp_trap_exception()
                else:
                    if processor.core_registers.scr.get_scd():
                        if processor.core_registers.is_secure():
                            print "unpredictable"
                        else:
                            raise UndefinedInstructionException()
                    else:
                        raise SMCException()
            else:
                raise UndefinedInstructionException()
