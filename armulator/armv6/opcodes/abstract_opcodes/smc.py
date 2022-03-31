from armulator.armv6.arm_exceptions import SMCException, UndefinedInstructionException
from armulator.armv6.configurations import have_security_ext, have_virt_ext
from armulator.armv6.opcodes.opcode import Opcode


class Smc(Opcode):
    def execute(self, processor):
        if processor.condition_passed():
            if have_security_ext() and processor.registers.current_mode_is_not_user():
                if (have_virt_ext() and not processor.registers.is_secure() and
                        not processor.registers.current_mode_is_hyp() and
                        processor.registers.hcr.tsc):
                    hsr_string = 0b0000000000000000000000000
                    processor.write_hsr(0b010011, hsr_string)
                    processor.registers.take_hyp_trap_exception()
                else:
                    if processor.registers.scr.scd:
                        if processor.registers.is_secure():
                            print('unpredictable')
                        else:
                            raise UndefinedInstructionException()
                    else:
                        raise SMCException()
            else:
                raise UndefinedInstructionException()
