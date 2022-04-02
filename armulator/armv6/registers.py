from enum import auto, Enum

from armulator.armv6 import bits_ops
from armulator.armv6 import shift
from armulator.armv6.all_registers.cpacr import CPACR
from armulator.armv6.all_registers.cpsr import CPSR
from armulator.armv6.all_registers.dacr import DACR
from armulator.armv6.all_registers.dbgdidr import DBGDIDR
from armulator.armv6.all_registers.dfsr import DFSR
from armulator.armv6.all_registers.fcseidr import FCSEIDR
from armulator.armv6.all_registers.fpexc import FPEXC
from armulator.armv6.all_registers.hcptr import HCPTR
from armulator.armv6.all_registers.hcr import HCR
from armulator.armv6.all_registers.hdcr import HDCR
from armulator.armv6.all_registers.hpfar import HPFAR
from armulator.armv6.all_registers.hsctlr import HSCTLR
from armulator.armv6.all_registers.hsr import HSR
from armulator.armv6.all_registers.hstr import HSTR
from armulator.armv6.all_registers.htcr import HTCR
from armulator.armv6.all_registers.id_pfr1 import IdPfr1
from armulator.armv6.all_registers.jmcr import JMCR
from armulator.armv6.all_registers.midr import MIDR
from armulator.armv6.all_registers.mpuir import MPUIR
from armulator.armv6.all_registers.nmrr import NMRR
from armulator.armv6.all_registers.nsacr import NSACR
from armulator.armv6.all_registers.pmcr import PMCR
from armulator.armv6.all_registers.prrr import PRRR
from armulator.armv6.all_registers.racr import DRACR, IRACR
from armulator.armv6.all_registers.rgnr import RGNR
from armulator.armv6.all_registers.rsr import DRSR, IRSR
from armulator.armv6.all_registers.scr import SCR
from armulator.armv6.all_registers.sctlr import SCTLR
from armulator.armv6.all_registers.sder import SDER
from armulator.armv6.all_registers.sunavcr import SUNAVCR
from armulator.armv6.all_registers.teecr import TEECR
from armulator.armv6.all_registers.ttbcr import TTBCR
from armulator.armv6.all_registers.vbar import VBAR
from armulator.armv6.all_registers.vtcr import VTCR
from armulator.armv6.bits_ops import chain, set_substring, bit_at, substring, set_bit_at
from armulator.armv6.configurations import *
from armulator.armv6.enums import *


class RName(Enum):
    R0usr = auto()
    R1usr = auto()
    R2usr = auto()
    R3usr = auto()
    R4usr = auto()
    R5usr = auto()
    R6usr = auto()
    R7usr = auto()
    R8usr = auto()
    R8fiq = auto()
    R9usr = auto()
    R9fiq = auto()
    R10usr = auto()
    R10fiq = auto()
    R11usr = auto()
    R11fiq = auto()
    R12usr = auto()
    R12fiq = auto()
    SPusr = auto()
    SPfiq = auto()
    SPirq = auto()
    SPsvc = auto()
    SPabt = auto()
    SPund = auto()
    SPmon = auto()
    SPhyp = auto()
    LRusr = auto()
    LRfiq = auto()
    LRirq = auto()
    LRsvc = auto()
    LRabt = auto()
    LRund = auto()
    LRmon = auto()
    PC = auto()


class Registers:
    def __init__(self):
        self._R = {}
        self.changed_registers = [False] * 16
        for register in RName:
            self._R[register] = 0
        self.cpsr = CPSR()
        self.spsr_hyp = 0b00000000000000000000000000000000
        self.spsr_svc = 0b00000000000000000000000000000000
        self.spsr_abt = 0b00000000000000000000000000000000
        self.spsr_und = 0b00000000000000000000000000000000
        self.spsr_mon = 0b00000000000000000000000000000000
        self.spsr_irq = 0b00000000000000000000000000000000
        self.spsr_fiq = 0b00000000000000000000000000000000
        self.elr_hyp = 0b00000000000000000000000000000000
        self.scr = SCR()
        self.nsacr = NSACR()
        self.sctlr = SCTLR()
        self.hstr = HSTR()
        self.hsr = HSR()
        self.hsctlr = HSCTLR()
        self.hvbar = 0b00000000000000000000000000000000
        self.jmcr = JMCR()
        self.hcr = HCR()
        self.mvbar = 0b00000000000000000000000000000000
        self.teehbr = 0b00000000000000000000000000000000
        self.hdcr = HDCR()
        self.vbar = VBAR()
        self.dbgdidr = DBGDIDR()
        self.dfsr = DFSR()
        self.dfar = 0b00000000000000000000000000000000
        self.hdfar = 0b00000000000000000000000000000000
        self.hpfar = HPFAR()
        self.ttbcr = TTBCR()
        self.fcseidr = FCSEIDR()
        self.htcr = HTCR()
        self.httbr = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.ttbr0_64 = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.ttbr1_64 = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.vtcr = VTCR()
        self.vttbr = 0b0000000000000000000000000000000000000000000000000000000000000000
        self.mair0 = 0b00000000000000000000000000000000
        self.mair1 = 0b00000000000000000000000000000000
        self.hmair0 = 0b00000000000000000000000000000000
        self.hmair1 = 0b00000000000000000000000000000000
        self.prrr = PRRR()
        self.nmrr = NMRR()
        self.dacr = DACR()
        self.mpuir = MPUIR()
        self.cpacr = CPACR()
        self.rgnr = RGNR(number_of_mpu_regions())
        self.hcptr = HCPTR()
        self.drsrs = [DRSR() for _ in range(number_of_mpu_regions())]
        self.drbars = [0] * number_of_mpu_regions()
        self.dracrs = [DRACR()for _ in range(number_of_mpu_regions())]
        self.irbars = [0] * number_of_mpu_regions()
        self.irsrs = [IRSR() for _ in range(number_of_mpu_regions())]
        self.iracrs = [IRACR() for _ in range(number_of_mpu_regions())]
        self.teecr = TEECR()
        self.event_register = False
        self.midr = MIDR()
        self.ctr = 0b00000000000000000000000000000000
        self.tcmtr = 0b00000000000000000000000000000000
        self.tlbtr = 0b00000000000000000000000000000000
        self.id_pfr0 = 0b00000000000000000000000000000000
        self.id_pfr1 = IdPfr1()
        self.id_dfr0 = 0b00000000000000000000000000000000
        self.id_afr0 = 0b00000000000000000000000000000000
        self.id_mmfr0 = 0b00000000000000000000000000000000
        self.id_mmfr1 = 0b00000000000000000000000000000000
        self.id_mmfr2 = 0b00000000000000000000000000000000
        self.id_mmfr3 = 0b00000000000000000000000000000000
        self.id_isar0 = 0b00000000000000000000000000000000
        self.id_isar1 = 0b00000000000000000000000000000000
        self.id_isar2 = 0b00000000000000000000000000000000
        self.id_isar3 = 0b00000000000000000000000000000000
        self.id_isar4 = 0b00000000000000000000000000000000
        self.id_isar5 = 0b00000000000000000000000000000000
        self.actlr = 0b00000000000000000000000000000000
        self.sder = SDER()
        self.ttbr0 = 0b00000000000000000000000000000000
        self.ttbr1 = 0b00000000000000000000000000000000
        self.ifsr = 0b00000000000000000000000000000000
        self.ifar = 0b00000000000000000000000000000000
        self.par = 0b00000000000000000000000000000000
        self.cdsr = 0b00000000000000000000000000000000
        self.dclr = 0b00000000000000000000000000000000
        self.iclr = 0b00000000000000000000000000000000
        self.dtcmrr = 0b00000000000000000000000000000000
        self.dtcm_nsacr = 0b00000000000000000000000000000000
        self.itcm_nsacr = 0b00000000000000000000000000000000
        self.tcmsr = 0b00000000000000000000000000000000
        self.cbor = 0b00000000000000000000000000000000
        self.tlblr = 0b00000000000000000000000000000000
        self.dmaispr = 0b00000000000000000000000000000000
        self.dmaisqr = 0b00000000000000000000000000000000
        self.dmaisrr = 0b00000000000000000000000000000000
        self.dmaisir = 0b00000000000000000000000000000000
        self.dmauar = 0b00000000000000000000000000000000
        self.dmacnr = 0b00000000000000000000000000000000
        self.stop_dmaer = 0b00000000000000000000000000000000
        self.start_dmaer = 0b00000000000000000000000000000000
        self.clear_dmaer = 0b00000000000000000000000000000000
        self.dmacr = 0b00000000000000000000000000000000
        self.dmaisar = 0b00000000000000000000000000000000
        self.dmaesar = 0b00000000000000000000000000000000
        self.dmaiear = 0b00000000000000000000000000000000
        self.dmacsr = 0b00000000000000000000000000000000
        self.dmacidr = 0b00000000000000000000000000000000
        self.isr = 0b00000000000000000000000000000000
        self.contextidr = 0b00000000000000000000000000000000
        self.tpidrurw = 0b00000000000000000000000000000000
        self.tpidruro = 0b00000000000000000000000000000000
        self.tpidrprw = 0b00000000000000000000000000000000
        self.ppmrr = 0b00000000000000000000000000000000
        self.sunavcr = SUNAVCR()
        self.pmcr = PMCR()
        self.ccr = 0b00000000000000000000000000000000
        self.cr0 = 0b00000000000000000000000000000000
        self.cr1 = 0b00000000000000000000000000000000
        self.svcr_rc = 0b00000000000000000000000000000000
        self.svcr_ic = 0b00000000000000000000000000000000
        self.svcr_fic = 0b00000000000000000000000000000000
        self.svcr_edrc = 0b00000000000000000000000000000000
        self.svcsmr = 0b00000000000000000000000000000000
        self.fpexc = FPEXC()

    def coproc_to_register(self, coproc, crn, opc1, crm, opc2):
        parameters_tuple = (coproc, crn, opc1, crm, opc2)
        coproc_to_register_dict = {
            (15, 0, 0, 0, 0): self.midr,
            (15, 0, 0, 0, 1): self.ctr,
            (15, 0, 0, 0, 2): self.tcmtr,
            (15, 0, 0, 1, 0): self.id_pfr0,
            (15, 0, 0, 1, 1): self.id_pfr1,
            (15, 0, 0, 1, 2): self.id_dfr0,
            (15, 0, 0, 1, 3): self.id_afr0,
            (15, 0, 0, 1, 4): self.id_mmfr0,
            (15, 0, 0, 1, 5): self.id_mmfr1,
            (15, 0, 0, 1, 6): self.id_mmfr2,
            (15, 0, 0, 1, 7): self.id_mmfr3,
            (15, 0, 0, 2, 0): self.id_isar0,
            (15, 0, 0, 2, 1): self.id_isar1,
            (15, 0, 0, 2, 2): self.id_isar2,
            (15, 0, 0, 2, 3): self.id_isar3,
            (15, 0, 0, 2, 4): self.id_isar4,
            (15, 0, 0, 2, 5): self.id_isar5,
            (15, 1, 0, 0, 0): self.sctlr,
            (15, 1, 0, 0, 1): self.actlr,
            (15, 1, 0, 0, 2): self.cpacr,
        }
        return coproc_to_register_dict[parameters_tuple]

    def pc_store_value(self):
        return self._R[RName.PC]

    def set_event_register(self, flag):
        self.event_register = flag

    def get_event_register(self):
        return self.event_register

    def current_instr_set(self) -> InstrSet:
        return InstrSet(self.cpsr.isetstate)

    def select_instr_set(self, iset: InstrSet):
        if iset == InstrSet.ARM and self.current_instr_set() == InstrSet.THUMB_EE:
            print('unpredictable')
            return
        self.cpsr.isetstate = iset.value

    def is_secure(self):
        return (not have_security_ext()) or (not self.scr.ns) or (self.cpsr.m == 0b10110)

    def bad_mode(self, mode):
        if mode == 0b10000:
            return False
        elif mode == 0b10001:
            return False
        elif mode == 0b10010:
            return False
        elif mode == 0b10011:
            return False
        elif mode == 0b10110:
            return not have_security_ext()
        elif mode == 0b10111:
            return False
        elif mode == 0b11010:
            return not have_virt_ext()
        elif mode == 0b11011:
            return False
        elif mode == 0b11111:
            return False
        return True

    def current_mode_is_not_user(self):
        if self.bad_mode(self.cpsr.m):
            print('unpredictable')
        if self.cpsr.m == 0b10000:
            return False
        return True

    def current_mode_is_hyp(self):
        if self.bad_mode(self.cpsr.m):
            print('unpredictable')
        if self.cpsr.m == 0b11010:
            return True
        return False

    def current_mode_is_user_or_system(self):
        if self.bad_mode(self.cpsr.m):
            print('unpredictable')
        if self.cpsr.m == 0b10000:
            return True
        if self.cpsr.m == 0b11111:
            return True
        return False

    def r_bank_select(self, mode, usr, fiq, irq, svc, abt, und, mon, hyp):
        if self.bad_mode(mode):
            print('unpredictable')
            return usr
        if mode == 0b10000:
            return usr
        elif mode == 0b10001:
            return fiq
        elif mode == 0b10010:
            return irq
        elif mode == 0b10011:
            return svc
        elif mode == 0b10110:
            return mon
        elif mode == 0b10111:
            return abt
        elif mode == 0b11010:
            return hyp
        elif mode == 0b11011:
            return und
        elif mode == 0b11111:
            return usr

    def r_fiq_bank_select(self, mode, usr, fiq):
        return self.r_bank_select(mode, usr, fiq, usr, usr, usr, usr, usr, usr)

    def look_up_rname(self, n, mode):
        assert 0 <= n <= 14
        if n == 0:
            return RName.R0usr
        elif n == 1:
            return RName.R1usr
        elif n == 2:
            return RName.R2usr
        elif n == 3:
            return RName.R3usr
        elif n == 4:
            return RName.R4usr
        elif n == 5:
            return RName.R5usr
        elif n == 6:
            return RName.R6usr
        elif n == 7:
            return RName.R7usr
        elif n == 8:
            return self.r_fiq_bank_select(mode, RName.R8usr, RName.R8fiq)
        elif n == 9:
            return self.r_fiq_bank_select(mode, RName.R9usr, RName.R9fiq)
        elif n == 10:
            return self.r_fiq_bank_select(mode, RName.R10usr, RName.R10fiq)
        elif n == 11:
            return self.r_fiq_bank_select(mode, RName.R11usr, RName.R11fiq)
        elif n == 12:
            return self.r_fiq_bank_select(mode, RName.R12usr, RName.R12fiq)
        elif n == 13:
            return self.r_bank_select(mode, RName.SPusr, RName.SPfiq, RName.SPirq, RName.SPsvc, RName.SPabt,
                                      RName.SPund, RName.SPmon, RName.SPhyp)
        elif n == 14:
            return self.r_bank_select(mode, RName.LRusr, RName.LRfiq, RName.LRirq, RName.LRsvc, RName.LRabt,
                                      RName.LRund, RName.LRmon, RName.LRusr)

    def get_rmode(self, n, mode):
        assert 0 <= n <= 14
        if not self.is_secure() and mode == 0b10110:
            print('unpredictable')
        if not self.is_secure() and mode == 0b10001 and self.nsacr.rfr:
            print('unpredictable')
        return self._R[self.look_up_rname(n, mode)]

    def set_rmode(self, n, mode, value):
        assert 0 <= n <= 14
        if not self.is_secure() and mode == 0b10110:
            print('unpredictable')
        if not self.is_secure() and mode == 0b10001 and self.nsacr.rfr:
            print('unpredictable')
        if n == 13 and bits_ops.lower_chunk(value, 2) != 0b00 and self.current_instr_set() != InstrSet.ARM:
            print('unpredictable')
        self._R[self.look_up_rname(n, mode)] = value

    def get(self, n):
        assert 0 <= n <= 15
        if n == 15:
            offset = 8 if (self.current_instr_set() == InstrSet.ARM) else 4
            result = bits_ops.add(self._R[RName.PC], offset, 32)
        else:
            result = self.get_rmode(n, self.cpsr.m)
        return result

    def set(self, n, value):
        assert 0 <= n <= 14
        self.changed_registers[n] = True
        self.set_rmode(n, self.cpsr.m, value)

    def get_sp(self):
        return self.get(13)

    def set_sp(self, value):
        self.set(13, value)

    def get_lr(self):
        return self.get(14)

    def set_lr(self, value):
        self.set(14, value)

    def get_pc(self):
        return self.get(15)

    def branch_to(self, address):
        self.changed_registers[15] = True
        self._R[RName.PC] = address

    def get_spsr(self):
        if self.bad_mode(self.cpsr.m):
            print('unpredictable')
            return 0x00000000
        if self.cpsr.m == 0b10001:
            return self.spsr_fiq
        elif self.cpsr.m == 0b10010:
            return self.spsr_irq
        elif self.cpsr.m == 0b10011:
            return self.spsr_svc
        elif self.cpsr.m == 0b10110:
            return self.spsr_mon
        elif self.cpsr.m == 0b10111:
            return self.spsr_abt
        elif self.cpsr.m == 0b11010:
            return self.spsr_hyp
        elif self.cpsr.m == 0b11011:
            return self.spsr_und
        print('unpredictable')
        return 0x00000000

    def set_spsr(self, value):
        if self.bad_mode(self.cpsr.m):
            print('unpredictable')
        else:
            if self.cpsr.m == 0b10001:
                self.spsr_fiq = value
            elif self.cpsr.m == 0b10010:
                self.spsr_irq = value
            elif self.cpsr.m == 0b10011:
                self.spsr_svc = value
            elif self.cpsr.m == 0b10110:
                self.spsr_mon = value
            elif self.cpsr.m == 0b10111:
                self.spsr_abt = value
            elif self.cpsr.m == 0b11010:
                self.spsr_hyp = value
            elif self.cpsr.m == 0b11011:
                self.spsr_und = value
            else:
                print('unpredictable')

    def it_advance(self):
        if bits_ops.lower_chunk(self.cpsr.it, 3) == 0b000:
            self.cpsr.it = 0
        else:
            itstate = self.cpsr.it
            mask, carry = shift.lsl_c(bits_ops.lower_chunk(itstate, 4), 4, 1)
            condition_state = chain(carry, mask, 4)
            self.cpsr.it = set_substring(itstate, 4, 0, condition_state)

    def cpsr_write_by_instr(self, value, bytemask, is_excp_return):
        privileged = self.current_mode_is_not_user()
        nmfi = self.sctlr.nmfi
        if bit_at(bytemask, 3):
            self.cpsr.value = set_substring(self.cpsr.value, 31, 27, substring(value, 31, 27))
            if is_excp_return:
                self.cpsr.value = set_substring(self.cpsr.value, 26, 24, substring(value, 26, 24))
        if bit_at(bytemask, 2):
            self.cpsr.value = set_substring(self.cpsr.value, 19, 16, substring(value, 19, 16))
        if bit_at(bytemask, 1):
            if is_excp_return:
                self.cpsr.value = set_substring(self.cpsr.value, 15, 10, substring(value, 15, 10))
            self.cpsr.value = set_bit_at(self.cpsr.value, 9, bit_at(value, 9))
            if privileged and (self.is_secure() or self.scr.aw or have_virt_ext()):
                self.cpsr.value = set_bit_at(self.cpsr.value, 8, bit_at(value, 8))
        if bit_at(bytemask, 0):
            if privileged:
                self.cpsr.value = set_bit_at(self.cpsr.value, 7, bit_at(value, 7))
            if (privileged and (not nmfi or not bit_at(value, 6)) and
                    (self.is_secure() or self.scr.fw or have_virt_ext())):
                self.cpsr.value = set_bit_at(self.cpsr.value, 6, bit_at(value, 6))
            if is_excp_return:
                self.cpsr.value = set_bit_at(self.cpsr.value, 5, bit_at(value, 5))
            if privileged:
                value_mode = substring(value, 4, 0)
                if self.bad_mode(value_mode):
                    print('unpredictable')
                else:
                    if not self.is_secure() and value_mode == 0b10110:
                        print('unpredictable')
                    elif not self.is_secure() and value_mode == 0b10001 and self.nsacr.rfr:
                        print('unpredictable')
                    elif not self.scr.ns and value_mode == 0b11010:
                        print('unpredictable')
                    elif not self.is_secure() and self.cpsr.m != 0b11010 and value_mode == 0b11010:
                        print('unpredictable')
                    elif self.cpsr.m == 0b11010 and value_mode != 0b11010 and not is_excp_return:
                        print('unpredictable')
                    else:
                        self.cpsr.m = value_mode

    def spsr_write_by_instr(self, value, bytemask):
        if self.current_mode_is_user_or_system():
            print('unpredictable')
        spsr = self.get_spsr()
        if bit_at(bytemask, 3):
            spsr = set_substring(spsr, 31, 27, substring(value, 31, 27))
        if bit_at(bytemask, 2):
            spsr = set_substring(spsr, 19, 16, substring(value, 19, 16))
        if bit_at(bytemask, 1):
            spsr = set_substring(spsr, 15, 8, substring(value, 15, 8))
        if bit_at(bytemask, 0):
            spsr = set_substring(spsr, 7, 5, substring(value, 7, 5))
            if self.bad_mode(substring(value, 4, 0)):
                print('unpredictable')
            else:
                spsr = set_substring(spsr, 4, 0, substring(value, 4, 0))
        self.set_spsr(spsr)

    def is_external_abort(self):
        # mock
        return False

    def is_async_abort(self):
        # mock
        return False

    def debug_exception(self):
        # mock
        return False

    def exc_vector_base(self):
        if self.sctlr.v:
            return 0xffff0000
        elif have_security_ext():
            return self.vbar.value
        else:
            return 0x00000000

    def enter_hyp_mode(self, new_spsr_value, preferred_exceptn_return, vect_offset):
        self.cpsr.m = 0b11010
        self.set_spsr(new_spsr_value)
        self.elr_hyp = preferred_exceptn_return
        self.cpsr.j = 0
        self.cpsr.t = self.hsctlr.te
        self.cpsr.e = self.hsctlr.ee
        if not self.scr.ea:
            self.cpsr.a = 1
        if not self.scr.fiq:
            self.cpsr.f = 1
        if not self.scr.irq:
            self.cpsr.i = 1
        self.cpsr.it = 0b00000000
        self.branch_to(self.hvbar + vect_offset)

    def enter_monitor_mode(self, new_spsr_value, new_lr_value, vect_offset):
        self.cpsr.m = 0b10110
        self.set_spsr(new_spsr_value)
        self.set(14, new_lr_value)
        self.cpsr.j = 0
        self.cpsr.t = self.sctlr.te
        self.cpsr.e = self.sctlr.ee
        self.cpsr.a = 1
        self.cpsr.f = 1
        self.cpsr.i = 1
        self.cpsr.it = 0b00000000
        self.branch_to(self.mvbar + vect_offset)

    def take_hyp_trap_exception(self):
        preferred_exceptn_return = self.get_pc() - 4 if self.cpsr.t else self.get_pc() - 8
        new_spsr_value = self.cpsr.value
        self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)

    def take_smc_exception(self):
        self.it_advance()
        new_lr_value = self.get_pc() if self.cpsr.t else self.get_pc() - 4
        new_spsr_value = self.cpsr.value
        vect_offset = 8
        if self.cpsr.m == 0b10110:
            self.scr.ns = 0
        self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)

    def take_data_abort_exception(self, dabort_exception):
        new_lr_value = bits_ops.add(self.get_pc(), 4, 32) if self.cpsr.t else self.get_pc()
        new_spsr_value = self.cpsr.value
        vect_offset = 16
        preferred_exceptn_return = bits_ops.sub(new_lr_value, 8, 32)
        route_to_monitor = have_security_ext() and self.scr.ea and self.is_external_abort()
        take_to_hyp = have_virt_ext() and have_security_ext() and self.scr.ns and self.cpsr.m == 0b11010
        route_to_hyp = (
                have_virt_ext() and
                have_security_ext() and
                not self.is_secure() and
                (
                        dabort_exception.second_stage_abort() or
                        (
                                self.cpsr.m != 0b11010 and
                                (self.is_external_abort() and self.is_async_abort() and self.hcr.amo) or
                                (self.debug_exception() and self.hdcr.tde)
                        ) or
                        (
                                self.cpsr.m == 0b10000 and
                                self.hcr.tge and
                                (dabort_exception.is_alignment_fault() or (
                                        self.is_external_abort() and not self.is_async_abort()))
                        )
                )
        )
        if route_to_monitor:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif take_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if have_security_ext() and self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.cpsr.m = 0b10111
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.i = 1
            if not have_security_ext() or have_virt_ext() or not self.scr.ns or self.scr.aw:
                self.cpsr.a = 1
            self.cpsr.it = 0b00000000
            self.cpsr.j = 0
            self.cpsr.t = self.sctlr.te
            self.cpsr.e = self.sctlr.ee
            self.branch_to(bits_ops.add(self.exc_vector_base(), vect_offset, 32))

    def take_undef_instr_exception(self):
        new_lr_value = bits_ops.sub(self.get_pc(), 2, 32) if self.cpsr.t else bits_ops.sub(self.get_pc(), 4, 32)
        new_spsr_value = self.cpsr.value
        vect_offset = 4
        take_to_hyp = have_virt_ext() and have_security_ext() and self.scr.ns and self.cpsr.m == 0b11010
        route_to_hyp = (have_virt_ext() and
                        have_security_ext() and
                        not self.is_secure() and
                        self.hcr.tge and
                        self.cpsr.m == 0b10000)
        return_offset = 2 if self.cpsr.t else 4
        preferred_exceptn_return = bits_ops.sub(new_lr_value, return_offset, 32)
        if take_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.cpsr.m = 0b11011
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.i = 1
            self.cpsr.it = 0b00000000
            self.cpsr.j = 0
            self.cpsr.t = self.sctlr.te
            self.cpsr.e = self.sctlr.ee
            self.branch_to(bits_ops.add(self.exc_vector_base(), vect_offset, 32))

    def take_svc_exception(self):
        self.it_advance()
        new_lr_value = bits_ops.sub(self.get_pc(), 2, 32) if self.cpsr.t else bits_ops.sub(self.get_pc(), 4, 32)
        new_spsr_value = self.cpsr.value
        vect_offset = 8
        take_to_hyp = have_virt_ext() and have_security_ext() and self.scr.ns and self.cpsr.m == 0b11010
        route_to_hyp = (have_virt_ext() and
                        have_security_ext() and
                        not self.is_secure() and
                        self.hcr.tge and
                        self.cpsr.m == 0b10000)
        preferred_exceptn_return = new_lr_value
        if take_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.cpsr.m = 0b10011
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.i = 1
            self.cpsr.it = 0b00000000
            self.cpsr.j = 0
            self.cpsr.t = self.sctlr.te
            self.cpsr.e = self.sctlr.ee
            self.branch_to(bits_ops.add(self.exc_vector_base(), vect_offset, 32))

    def take_physical_irq_exception(self):
        new_lr_value = self.get_pc() if self.cpsr.t else bits_ops.sub(self.get_pc(), 4, 32)
        new_spsr_value = self.cpsr.value
        vect_offset = 24
        route_to_monitor = have_security_ext() and self.scr.irq
        route_to_hyp = (
                (have_virt_ext() and
                 have_security_ext() and
                 not self.scr.irq and
                 self.hcr.imo and
                 not self.is_secure()) or
                self.cpsr.m == 0b11010
        )
        if route_to_monitor:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif route_to_hyp:
            self.hsr.value = 0x00000000  # unknown
            preferred_exceptn_return = bits_ops.sub(new_lr_value, 4, 32)
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        else:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.cpsr.m = 0b10010
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.i = 1
            if not have_security_ext() or have_virt_ext() or not self.scr.ns or self.scr.aw:
                self.cpsr.a = 1
            self.cpsr.it = 0b00000000
            self.cpsr.j = 0
            self.cpsr.t = self.sctlr.te
            self.cpsr.e = self.sctlr.ee
            if self.sctlr.ve:
                self.branch_to(configurations.impdef_irq_vector)
            else:
                self.branch_to(bits_ops.add(self.exc_vector_base(), vect_offset, 32))

    def take_physical_fiq_exception(self):
        new_lr_value = self.get_pc() if self.cpsr.t else bits_ops.sub(self.get_pc(), 4, 32)
        new_spsr_value = self.cpsr.value
        vect_offset = 28
        route_to_monitor = have_security_ext() and self.scr.fiq
        route_to_hyp = (
                (have_virt_ext() and
                 have_security_ext() and
                 not self.scr.fiq and
                 self.hcr.fmo and
                 not self.is_secure()) or
                self.cpsr.m == 0b11010
        )
        if route_to_monitor:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif route_to_hyp:
            self.hsr.value = 0x00000000  # unknown
            preferred_exceptn_return = bits_ops.sub(new_lr_value, 4, 32)
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        else:
            if self.cpsr.m == 0b10110:
                self.scr.ns = 0
            self.cpsr.m = 0b10001
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.i = 1
            if not have_security_ext() or have_virt_ext() or not self.scr.ns or self.scr.fw:
                self.cpsr.f = 1
            if not have_security_ext() or have_virt_ext() or not self.scr.ns or self.scr.aw:
                self.cpsr.a = 1
            self.cpsr.it = 0b00000000
            self.cpsr.j = 0
            self.cpsr.t = self.sctlr.te
            self.cpsr.e = self.sctlr.ee
            if self.sctlr.ve:
                self.branch_to(configurations.impdef_fiq_vector)
            else:
                self.branch_to(bits_ops.add(self.exc_vector_base(), vect_offset, 32))

    def increment_pc(self, opcode_length):
        self._R[RName.PC] = bits_ops.add(self._R[RName.PC], opcode_length, 32)

    def reset_control_registers(self):
        self.vbar = VBAR()
