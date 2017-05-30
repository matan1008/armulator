from bitstring import BitArray
from enum import Enum
from configurations import *
import shift
import bits_ops
import implementation_defined
from arm_exceptions import *
from enums import *
from armulator.all_registers.sunavcr import SUNAVCR
from armulator.all_registers.pmcr import PMCR
from armulator.all_registers.jmcr import JMCR
from armulator.all_registers.prrr import PRRR
from armulator.all_registers.nmrr import NMRR
from armulator.all_registers.dacr import DACR
from armulator.all_registers.mpuir import MPUIR
from armulator.all_registers.cpacr import CPACR
from armulator.all_registers.scr import SCR
from armulator.all_registers.nsacr import NSACR
from armulator.all_registers.rgnr import RGNR
from armulator.all_registers.teecr import TEECR
from armulator.all_registers.midr import MIDR
from armulator.all_registers.vbar import VBAR
from armulator.all_registers.ttbcr import TTBCR
from armulator.all_registers.sctlr import SCTLR
from armulator.all_registers.hstr import HSTR
from armulator.all_registers.hsctlr import HSCTLR
from armulator.all_registers.hcr import HCR
from armulator.all_registers.hdcr import HDCR
from armulator.all_registers.htcr import HTCR
from armulator.all_registers.vtcr import VTCR
from armulator.all_registers.hcptr import HCPTR
from armulator.all_registers.rsr import DRSR, IRSR
from armulator.all_registers.racr import DRACR, IRACR
from armulator.all_registers.sder import SDER
from armulator.all_registers.fcseidr import FCSEIDR
from armulator.all_registers.fpexc import FPEXC
from armulator.all_registers.hsr import HSR
from armulator.all_registers.dbgdidr import DBGDIDR
from armulator.all_registers.hpfar import HPFAR
from armulator.all_registers.dfsr import DFSR
from armulator.all_registers.cpsr import CPSR


class Registers:
    def __init__(self):
        rnames = ("RName_0usr RName_1usr RName_2usr RName_3usr RName_4usr RName_5usr RName_6usr RName_7usr "
                  "RName_8usr RName_8fiq RName_9usr RName_9fiq RName_10usr RName_10fiq RName_11usr RName_11fiq "
                  "RName_12usr RName_12fiq RName_SPusr RName_SPfiq RName_SPirq RName_SPsvc RName_SPabt RName_SPund "
                  "RName_SPmon RName_SPhyp RName_LRusr RName_LRfiq RName_LRirq RName_LRsvc RName_LRabt RName_LRund "
                  "RName_LRmon RName_PC")
        self.RName = Enum("RName", rnames)
        self._R = {}
        self.changed_registers = [False] * 16
        for register in self.RName:
            self._R[register] = BitArray(length=32)
        self.cpsr = CPSR()
        self.spsr_hyp = BitArray(length=32)
        self.spsr_svc = BitArray(length=32)
        self.spsr_abt = BitArray(length=32)
        self.spsr_und = BitArray(length=32)
        self.spsr_mon = BitArray(length=32)
        self.spsr_irq = BitArray(length=32)
        self.spsr_fiq = BitArray(length=32)
        self.elr_hyp = BitArray(length=32)
        self.scr = SCR()
        self.nsacr = NSACR()
        self.sctlr = SCTLR()
        self.hstr = HSTR()
        self.hsr = HSR()
        self.hsctlr = HSCTLR()
        self.hvbar = BitArray(length=32)
        self.jmcr = JMCR()
        self.hcr = HCR()
        self.mvbar = BitArray(length=32)
        self.teehbr = BitArray(length=32)
        self.hdcr = HDCR()
        self.vbar = VBAR()
        self.dbgdidr = DBGDIDR()
        self.dfsr = DFSR()
        self.dfar = BitArray(length=32)
        self.hdfar = BitArray(length=32)
        self.hpfar = HPFAR()
        self.ttbcr = TTBCR()
        self.fcseidr = FCSEIDR()
        self.htcr = HTCR()
        self.httbr = BitArray(length=64)
        self.ttbr0_64 = BitArray(length=64)
        self.ttbr1_64 = BitArray(length=64)
        self.vtcr = VTCR()
        self.vttbr = BitArray(length=64)
        self.mair0 = BitArray(length=32)
        self.mair1 = BitArray(length=32)
        self.hmair0 = BitArray(length=32)
        self.hmair1 = BitArray(length=32)
        self.prrr = PRRR()
        self.nmrr = NMRR()
        self.dacr = DACR()
        self.mpuir = MPUIR()
        self.cpacr = CPACR()
        self.rgnr = RGNR(number_of_mpu_regions)
        self.hcptr = HCPTR()
        self.drsrs = [DRSR()] * number_of_mpu_regions
        self.drbars = [BitArray(length=32)] * number_of_mpu_regions
        self.dracrs = [DRACR()] * number_of_mpu_regions
        self.irbars = [BitArray(length=32)] * number_of_mpu_regions
        self.irsrs = [IRSR()] * number_of_mpu_regions
        self.iracrs = [IRACR()] * number_of_mpu_regions
        self.teecr = TEECR()
        self.event_register = False
        self.midr = MIDR()
        self.ctr = BitArray(length=32)
        self.tcmtr = BitArray(length=32)
        self.tlbtr = BitArray(length=32)
        self.id_pfr0 = BitArray(length=32)
        self.id_pfr1 = BitArray(length=32)
        self.id_dfr0 = BitArray(length=32)
        self.id_afr0 = BitArray(length=32)
        self.id_mmfr0 = BitArray(length=32)
        self.id_mmfr1 = BitArray(length=32)
        self.id_mmfr2 = BitArray(length=32)
        self.id_mmfr3 = BitArray(length=32)
        self.id_isar0 = BitArray(length=32)
        self.id_isar1 = BitArray(length=32)
        self.id_isar2 = BitArray(length=32)
        self.id_isar3 = BitArray(length=32)
        self.id_isar4 = BitArray(length=32)
        self.id_isar5 = BitArray(length=32)
        self.actlr = BitArray(length=32)
        self.sder = SDER()
        self.ttbr0 = BitArray(length=32)
        self.ttbr1 = BitArray(length=32)
        self.ifsr = BitArray(length=32)
        self.ifar = BitArray(length=32)
        self.par = BitArray(length=32)
        self.cdsr = BitArray(length=32)
        self.dclr = BitArray(length=32)
        self.iclr = BitArray(length=32)
        self.dtcmrr = BitArray(length=32)
        self.dtcm_nsacr = BitArray(length=32)
        self.itcm_nsacr = BitArray(length=32)
        self.tcmsr = BitArray(length=32)
        self.cbor = BitArray(length=32)
        self.tlblr = BitArray(length=32)
        self.dmaispr = BitArray(length=32)
        self.dmaisqr = BitArray(length=32)
        self.dmaisrr = BitArray(length=32)
        self.dmaisir = BitArray(length=32)
        self.dmauar = BitArray(length=32)
        self.dmacnr = BitArray(length=32)
        self.stop_dmaer = BitArray(length=32)
        self.start_dmaer = BitArray(length=32)
        self.clear_dmaer = BitArray(length=32)
        self.dmacr = BitArray(length=32)
        self.dmaisar = BitArray(length=32)
        self.dmaesar = BitArray(length=32)
        self.dmaiear = BitArray(length=32)
        self.dmacsr = BitArray(length=32)
        self.dmacidr = BitArray(length=32)
        self.isr = BitArray(length=32)
        self.contextidr = BitArray(length=32)
        self.tpidrurw = BitArray(length=32)
        self.tpidruro = BitArray(length=32)
        self.tpidrprw = BitArray(length=32)
        self.ppmrr = BitArray(length=32)
        self.sunavcr = SUNAVCR()
        self.pmcr = PMCR()
        self.ccr = BitArray(length=32)
        self.cr0 = BitArray(length=32)
        self.cr1 = BitArray(length=32)
        self.svcr_rc = BitArray(length=32)
        self.svcr_ic = BitArray(length=32)
        self.svcr_fic = BitArray(length=32)
        self.svcr_edrc = BitArray(length=32)
        self.svcsmr = BitArray(length=32)
        self.fpexc = FPEXC()

    def coproc_register_name(self, coproc, crn, opc1, crm, opc2):
        if coproc == 15:
            if crn == 0:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "MIDR"
                        elif opc2 == 1:
                            return "ctr"
                        elif opc2 == 2:
                            return "tcmtr"
                        elif opc2 == 3:
                            return "tlbtr"
                    elif crm == 1:
                        if opc2 == 0:
                            return "id_pfr0"
                        elif opc2 == 1:
                            return "id_pfr1"
                        elif opc2 == 2:
                            return "id_dfr0"
                        elif opc2 == 3:
                            return "id_afr0"
                        elif opc2 == 4:
                            return "id_mmfr0"
                        elif opc2 == 5:
                            return "id_mmfr1"
                        elif opc2 == 6:
                            return "id_mmfr2"
                        elif opc2 == 7:
                            return "id_mmfr3"
                    elif crm == 2:
                        if opc2 == 0:
                            return "id_isar0"
                        elif opc2 == 1:
                            return "id_isar1"
                        elif opc2 == 2:
                            return "id_isar2"
                        elif opc2 == 3:
                            return "id_isar3"
                        elif opc2 == 4:
                            return "id_isar4"
                        elif opc2 == 5:
                            return "id_isar5"
            elif crn == 1:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "SCTLR"
                        elif opc2 == 1:
                            return "actlr"
                        elif opc2 == 2:
                            return "CPACR"
                    elif crm == 1:
                        if opc2 == 0:
                            return "SCR"
                        elif opc2 == 1:
                            return "SDER"
                        elif opc2 == 2:
                            return "NSACR"
            elif crn == 2:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "ttbr0"
                        elif opc2 == 1:
                            return "ttbr1"
                        elif opc2 == 2:
                            return "TTBCR"
            elif crn == 3:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "DACR"
            elif crn == 5:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "DFSR"
                        elif opc2 == 1:
                            return "ifsr"
            elif crn == 6:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "dfar"
                        elif opc2 == 2:
                            return "ifar"
            elif crn == 7:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 4:
                            return "CP15WFI"
                    elif crm == 4:
                        if opc2 == 0:
                            return "par"
                    elif crm == 5:
                        if opc2 == 0:
                            return "ICIALLU"
                        elif opc2 == 1:
                            return "ICIMVAU"
                        elif opc2 == 2:
                            return "ICISW"
                        elif opc2 == 4:
                            return "CP15ISB"
                        elif opc2 == 6:
                            return "BPIALL"
                        elif opc2 == 7:
                            return "BPIMVA"
                    elif crm == 6:
                        if opc2 == 0:
                            return "DCIALL"
                        elif opc2 == 1:
                            return "DCIMVAC"
                        elif opc2 == 2:
                            return "DCISW"
                    elif crm == 7:
                        if opc2 == 0:
                            return "Invalidate Both Caches"
                    elif crm == 8:
                        if opc2 == 0:
                            return "ATS1CPR"
                        elif opc2 == 1:
                            return "ATS1CPW"
                        elif opc2 == 2:
                            return "ATS1CUR"
                        elif opc2 == 3:
                            return "ATS1CUW"
                        elif opc2 == 4:
                            return "ATS12NSOPR"
                        elif opc2 == 5:
                            return "ATS12NSOPW"
                        elif opc2 == 6:
                            return "ATS12NSOUR"
                        elif opc2 == 7:
                            return "ATS12NSOUW"
                    elif crm == 10:
                        if opc2 == 0:
                            return "DCCALL"
                        elif opc2 == 1:
                            return "DCCMVAC"
                        elif opc2 == 2:
                            return "DCCSW"
                        elif opc2 == 4:
                            return "CP15DSB"
                        elif opc2 == 5:
                            return "CP15DMB"
                        elif opc2 == 6:
                            return "cdsr"
                    elif crm == 13:
                        if opc2 == 1:
                            return "Prefetch Instruction Cache Line"
                    elif crm == 14:
                        if opc2 == 0:
                            return "DCCIALL"
                        elif opc2 == 1:
                            return "DCCIMVAC"
                        elif opc2 == 2:
                            return "DCCISW"
            elif crn == 8:
                if opc1 == 0:
                    if crm == 5:
                        if opc2 == 0:
                            return "Invalidate Instruction TLB unlocked entries"
                        elif opc2 == 1:
                            return "Invalidate Instruction TLB entry by MVA"
                        elif opc2 == 2:
                            return "Invalidate Instruction TLB entry on ASID match"
                    elif crm == 6:
                        if opc2 == 0:
                            return "Invalidate Data TLB unlocked entries"
                        elif opc2 == 1:
                            return "Invalidate Data TLB entry by MVA"
                        elif opc2 == 2:
                            return "Invalidate Data TLB entry on ASID match"
                    elif crm == 7:
                        if opc2 == 0:
                            return "Invalidate unified TLB unlocked entries"
                        elif opc2 == 1:
                            return "Invalidate unified TLB entry by MVA"
                        elif opc2 == 2:
                            return "Invalidate unified TLB entry on ASID match"
            elif crn == 9:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "dclr"
                        elif opc2 == 0:
                            return "iclr"
                    elif crm == 1:
                        if opc2 == 0:
                            return "dtcmrr"
                        elif opc2 == 1:
                            return "ITCMRR"
                        elif opc2 == 2:
                            return "dtcm_nsacr"
                        elif opc2 == 3:
                            return "itcm_nsacr"
                    elif crm == 2:
                        if opc2 == 0:
                            return "tcmsr"
                    elif crm == 8:
                        if opc2 == 0:
                            return "cbor"
            elif crn == 10:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "tlblr"
                    elif crm == 2:
                        if opc2 == 0:
                            return "PRRR"
                        elif opc2 == 1:
                            return "NMRR"
            elif crn == 11:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "dmaispr"
                        elif opc2 == 1:
                            return "dmaisqr"
                        elif opc2 == 2:
                            return "dmaisrr"
                        elif opc2 == 3:
                            return "dmaisir"
                    elif crm == 1:
                        if opc2 == 0:
                            return "dmauar"
                    elif crm == 2:
                        if opc2 == 0:
                            return "dmacnr"
                    elif crm == 3:
                        if opc2 == 0:
                            return "stop_dmaer"
                        elif opc2 == 1:
                            return "start_dmaer"
                        elif opc2 == 2:
                            return "clear_dmaer"
                    elif crm == 4:
                        if opc2 == 0:
                            return "dmacr"
                    elif crm == 5:
                        if opc2 == 0:
                            return "dmaisar"
                    elif crm == 6:
                        if opc2 == 0:
                            return "dmaesar"
                    elif crm == 7:
                        if opc2 == 0:
                            return "dmaiear"
                    elif crm == 8:
                        if opc2 == 0:
                            return "dmacsr"
                    elif crm == 8:
                        if opc2 == 0:
                            return "dmacidr"
            elif crn == 12:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "VBAR"
                        elif opc2 == 1:
                            return "mvbar"
                    elif crm == 1:
                        if opc2 == 0:
                            return "isr"
            elif crn == 13:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "FCSEIDR"
                        elif opc2 == 1:
                            return "contextidr"
                        elif opc2 == 2:
                            return "tpidrurw"
                        elif opc2 == 3:
                            return "tpidruro"
                        elif opc2 == 4:
                            return "tpidrprw"
            elif crn == 15:
                if opc1 == 0:
                    if crm == 2:
                        if opc2 == 4:
                            return "ppmrr"
                    elif crm == 9:
                        if opc2 == 0:
                            return "SUNAVCR"
                    elif crm == 12:
                        if opc2 == 0:
                            return "PMCR"
                        elif opc2 == 1:
                            return "ccr"
                        elif opc2 == 2:
                            return "cr0"
                        elif opc2 == 3:
                            return "cr1"
                        elif opc2 == 4:
                            return "svcr_rc"
                        elif opc2 == 5:
                            return "svcr_ic"
                        elif opc2 == 6:
                            return "svcr_fic"
                        elif opc2 == 7:
                            return "svcr_edrc"
                    elif crm == 13:
                        if opc2 == 1:
                            return "Start reset counter"
                        elif opc2 == 2:
                            return "Start interrupt counter"
                        elif opc2 == 3:
                            return " Start reset and interrupt counters"
                        elif opc2 == 4:
                            return "Start fast interrupt counter"
                        elif opc2 == 5:
                            return "Start reset and fast interrupt counters"
                        elif opc2 == 6:
                            return " Start interrupt and fast interrupt counters"
                        elif opc2 == 7:
                            return "Start reset, interrupt and fast interrupt counters"
                    elif crm == 14:
                        if opc2 == 0:
                            return "svcsmr"
                elif opc1 == 1:
                    if crm == 13:
                        # unknown
                        pass

    def pc_store_value(self):
        # not sure
        return self._R[self.RName.RName_PC]

    def set_event_register(self, flag):
        self.event_register = flag

    def get_event_register(self):
        return self.event_register

    def current_instr_set(self):
        isetstate = self.cpsr.get_isetstate()
        if isetstate == "0b00":
            result = InstrSet.InstrSet_ARM
        if isetstate == "0b01":
            result = InstrSet.InstrSet_Thumb
        if isetstate == "0b10":
            result = InstrSet.InstrSet_Jazelle
        if isetstate == "0b11":
            result = InstrSet.InstrSet_ThumbEE
        return result

    def select_instr_set(self, iset):
        if iset == InstrSet.InstrSet_ARM:
            if self.current_instr_set() == InstrSet.InstrSet_ThumbEE:
                print "unpredictable"
            else:
                self.cpsr.set_isetstate("0b00")
        if iset == InstrSet.InstrSet_Thumb:
            self.cpsr.set_isetstate("0b01")
        if iset == InstrSet.InstrSet_Jazelle:
            self.cpsr.set_isetstate("0b10")
        if iset == InstrSet.InstrSet_ThumbEE:
            self.cpsr.set_isetstate("0b11")

    def is_secure(self):
        return (not HaveSecurityExt()) or (not self.scr.get_ns()) or (self.cpsr.get_m() == "0b10110")

    def bad_mode(self, mode):
        if mode.bin == "10000":
            result = False
        elif mode.bin == "10001":
            result = False
        elif mode.bin == "10010":
            result = False
        elif mode.bin == "10011":
            result = False
        elif mode.bin == "10110":
            result = not HaveSecurityExt()
        elif mode.bin == "10111":
            result = False
        elif mode.bin == "11010":
            result = not HaveVirtExt()
        elif mode.bin == "11011":
            result = False
        elif mode.bin == "11111":
            result = False
        else:
            result = True
        return result

    def current_mode_is_not_user(self):
        if self.bad_mode(self.cpsr.get_m()):
            print "unpredictable"
        if self.cpsr.get_m() == "0b10000":
            return False
        return True

    def current_mode_is_hyp(self):
        if self.bad_mode(self.cpsr.get_m()):
            print "unpredictable"
        if self.cpsr.get_m() == "0b11010":
            return True
        return False

    def current_mode_is_user_or_system(self):
        if self.bad_mode(self.cpsr.get_m()):
            print "unpredictable"
        if self.cpsr.get_m() == "0b10000":
            return True
        if self.cpsr.get_m() == "0b11111":
            return True
        return False

    def r_bank_select(self, mode, usr, fiq, irq, svc, abt, und, mon, hyp):
        if self.bad_mode(mode):
            print "unpredictable"
            result = usr
        else:
            if mode.bin == "10000":
                result = usr
            elif mode.bin == "10001":
                result = fiq
            elif mode.bin == "10010":
                result = irq
            elif mode.bin == "10011":
                result = svc
            elif mode.bin == "10110":
                result = mon
            elif mode.bin == "10111":
                result = abt
            elif mode.bin == "11010":
                result = hyp
            elif mode.bin == "11011":
                result = und
            elif mode.bin == "11111":
                result = usr
        return result

    def r_fiq_bank_select(self, mode, usr, fiq):
        return self.r_bank_select(mode, usr, fiq, usr, usr, usr, usr, usr, usr)

    def look_up_rname(self, n, mode):
        assert 0 <= n <= 14
        if n is 0:
            result = self.RName.RName_0usr
        elif n is 1:
            result = self.RName.RName_1usr
        elif n is 2:
            result = self.RName.RName_2usr
        elif n is 3:
            result = self.RName.RName_3usr
        elif n is 4:
            result = self.RName.RName_4usr
        elif n is 5:
            result = self.RName.RName_5usr
        elif n is 6:
            result = self.RName.RName_6usr
        elif n is 7:
            result = self.RName.RName_7usr
        elif n is 8:
            result = self.r_fiq_bank_select(mode, self.RName.RName_8usr, self.RName.RName_8fiq)
        elif n is 9:
            result = self.r_fiq_bank_select(mode, self.RName.RName_9usr, self.RName.RName_9fiq)
        elif n is 10:
            result = self.r_fiq_bank_select(mode, self.RName.RName_10usr, self.RName.RName_10fiq)
        elif n is 11:
            result = self.r_fiq_bank_select(mode, self.RName.RName_11usr, self.RName.RName_11fiq)
        elif n is 12:
            result = self.r_fiq_bank_select(mode, self.RName.RName_12usr, self.RName.RName_12fiq)
        elif n is 13:
            result = self.r_bank_select(mode, self.RName.RName_SPusr, self.RName.RName_SPfiq,
                                        self.RName.RName_SPirq, self.RName.RName_SPsvc, self.RName.RName_SPabt,
                                        self.RName.RName_SPund, self.RName.RName_SPmon, self.RName.RName_SPhyp)
        elif n is 14:
            result = self.r_bank_select(mode, self.RName.RName_LRusr, self.RName.RName_LRfiq,
                                        self.RName.RName_LRirq, self.RName.RName_LRsvc, self.RName.RName_LRabt,
                                        self.RName.RName_LRund, self.RName.RName_LRmon, self.RName.RName_LRusr)
        return result

    def get_rmode(self, n, mode):
        assert 0 <= n <= 14
        if not self.is_secure() and mode.bin == "10110":
            print "unpredictable"
        if not self.is_secure() and mode.bin == "10001" and self.nsacr.get_rfr():
            print "unpredictable"
        return self._R[self.look_up_rname(n, mode)]

    def set_rmode(self, n, mode, value):
        assert 0 <= n <= 14
        if not self.is_secure() and mode.bin == "10110":
            print "unpredictable"
        if not self.is_secure() and mode.bin == "10001" and self.nsacr.get_rfr():
            print "unpredictable"
        if n == 13 and value.bin[30:32] != "00" and self.current_instr_set() != InstrSet.InstrSet_ARM:
            print "unpredictable"
        self._R[self.look_up_rname(n, mode)] = value

    def get(self, n):
        assert 0 <= n <= 15
        if n == 15:
            offset = "1000" if (self.current_instr_set() == InstrSet.InstrSet_ARM) else "100"
            result = bits_ops.add(self._R[self.RName.RName_PC], BitArray(bin=offset), 32)
        else:
            result = self.get_rmode(n, self.cpsr.get_m())
        return result

    def set(self, n, value):
        assert 0 <= n <= 14
        self.changed_registers[n] = True
        self.set_rmode(n, self.cpsr.get_m(), value)

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
        self._R[self.RName.RName_PC] = address

    def get_spsr(self):
        if self.bad_mode(self.cpsr.get_m()):
            print "unpredictable"
            result = BitArray(length=32)
        else:
            result = BitArray(length=32)
            if self.cpsr.get_m() == "0b10001":
                result = self.spsr_fiq
            elif self.cpsr.get_m() == "0b10010":
                result = self.spsr_irq
            elif self.cpsr.get_m() == "0b10011":
                result = self.spsr_svc
            elif self.cpsr.get_m() == "0b10110":
                result = self.spsr_mon
            elif self.cpsr.get_m() == "0b10111":
                result = self.spsr_abt
            elif self.cpsr.get_m() == "0b11010":
                result = self.spsr_hyp
            elif self.cpsr.get_m() == "0b11011":
                result = self.spsr_und
            else:
                print "unpredictable"
        return result

    def set_spsr(self, value):
        if self.bad_mode(self.cpsr.get_m()):
            print "unpredictable"
        else:
            if self.cpsr.get_m() == "0b10001":
                self.spsr_fiq = value
            elif self.cpsr.get_m() == "0b10010":
                self.spsr_irq = value
            elif self.cpsr.get_m() == "0b10011":
                self.spsr_svc = value
            elif self.cpsr.get_m() == "0b10110":
                self.spsr_mon = value
            elif self.cpsr.get_m() == "0b10111":
                self.spsr_abt = value
            elif self.cpsr.get_m() == "0b11010":
                self.spsr_hyp = value
            elif self.cpsr.get_m() == "0b11011":
                self.spsr_und = value
            else:
                print "unpredictable"

    def it_advance(self):
        if self.cpsr.get_it()[-3:] == "0b000":
            self.cpsr.set_it("0b00000000")
        else:
            itstate = self.cpsr.get_it()
            itstate.overwrite(shift.lsl(itstate[4:], 1), 4)

    def cpsr_write_by_instr(self, value, bytemask, is_excp_return):
        privileged = self.current_mode_is_not_user()
        nmfi = self.sctlr.get_nmfi()
        if bytemask[0]:
            self.cpsr.value.overwrite(value[0:5], 0)
            if is_excp_return:
                self.cpsr.value.overwrite(value[5:8], 5)
        if bytemask[1]:
            self.cpsr.set_ge(value[12:16])
        if bytemask[2]:
            if is_excp_return:
                self.cpsr.value.overwrite(value[16:22], 16)
            self.cpsr.set_e(value[22])
            if privileged and (self.is_secure() or self.scr.get_aw() or HaveVirtExt()):
                self.cpsr.set_a(value[23])
        if bytemask[3]:
            if privileged:
                self.cpsr.set_i(value[24])
            if privileged and (not nmfi or not value[25]) and (self.is_secure() or self.scr.get_fw() or HaveVirtExt()):
                self.cpsr.set_f(value[25])
            if is_excp_return:
                self.cpsr.set_t(value[26])
            if privileged:
                if self.bad_mode(value[27:]):
                    print "unpredictable"
                else:
                    if not self.is_secure() and value.bin[27:] == "10110":
                        print "unpredictable"
                    elif not self.is_secure() and value.bin[27:] == "10001" and self.nsacr.get_rfr():
                        print "unpredictable"
                    elif not self.scr.get_ns() and value.bin[27:] == "11010":
                        print "unpredictable"
                    elif not self.is_secure() and self.cpsr.get_m() != "0b11010" and value.bin[27:] == "11010":
                        print "unpredictable"
                    elif self.cpsr.get_m() == "0b11010" and value.bin[27:] != "11010" and not is_excp_return:
                        print "unpredictable"
                    else:
                        self.cpsr.set_m(value[27:32])

    def spsr_write_by_instr(self, value, bytemask):
        if self.current_mode_is_user_or_system():
            print "unpredictable"
        spsr = self.get_spsr()
        if bytemask[0]:
            spsr.overwrite(value[0:5], 0)
        if bytemask[1]:
            spsr.overwrite(value[12:16], 12)
        if bytemask[2]:
            spsr.overwrite(value[16:24], 16)
        if bytemask[3]:
            spsr.overwrite(value[24:27], 24)
            if self.bad_mode(value[27:]):
                print "unpredictable"
            else:
                spsr.overwrite(value[27:], 27)
        self.set_spsr(spsr)

    def is_external_abort(self):
        # mock
        return False

    def second_stage_abort(self):
        # mock
        return False

    def is_async_abort(self):
        # mock
        return False

    def debug_exception(self):
        # mock
        return False

    def is_alignment_fault(self):
        # mock
        return False

    def exc_vector_base(self):
        if self.sctlr.get_v():
            return BitArray(bin="11111111111111110000000000000000")
        elif HaveSecurityExt():
            return self.vbar.value
        else:
            return BitArray(length=32)

    def enter_hyp_mode(self, new_spsr_value, preferred_exceptn_return, vect_offset):
        self.cpsr.set_m("0b11010")
        self.set_spsr(new_spsr_value)
        self.elr_hyp = preferred_exceptn_return
        self.cpsr.set_j(False)
        self.cpsr.set_t(self.hsctlr.get_te())
        self.cpsr.set_e(self.hsctlr.get_ee())
        if not self.scr.get_ea():
            self.cpsr.set_a(True)
        if not self.scr.get_fiq():
            self.cpsr.set_f(True)
        if not self.scr.get_irq():
            self.cpsr.set_i(True)
        self.cpsr.set_it(BitArray(length=8))
        self.branch_to(BitArray(uint=(self.hvbar.uint + vect_offset), length=32))

    def enter_monitor_mode(self, new_spsr_value, new_lr_value, vect_offset):
        self.cpsr.set_m("0b10110")
        self.set_spsr(new_spsr_value)
        self.set(14, new_lr_value)
        self.cpsr.set_j(False)
        self.cpsr.set_t(self.sctlr.get_te())
        self.cpsr.set_e(self.sctlr.get_ee())
        self.cpsr.set_a(True)
        self.cpsr.set_f(True)
        self.cpsr.set_i(True)
        self.cpsr.set_it(BitArray(length=8))
        self.branch_to(BitArray(uint=(self.mvbar.uint + vect_offset), length=32))

    def take_hyp_trap_exception(self):
        preferred_exceptn_return = BitArray(
            uint=(self.get_pc().uint - 4 if self.cpsr.get_t() else self.get_pc().uint - 8), length=32)
        new_spsr_value = self.cpsr.value
        self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)

    def take_smc_exception(self):
        self.it_advance()
        new_lr_value = self.get_pc() if self.cpsr.get_t() else BitArray(uint=(self.get_pc().uint - 4), length=32)
        new_spsr_value = self.cpsr.value
        vect_offset = 8
        if self.cpsr.get_m() == "0b10110":
            self.scr.set_ns(False)
        self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)

    def take_data_abort_exception(self):
        new_lr_value = BitArray(uint=self.get_pc().uint + 4, length=32) if self.cpsr.get_t() else self.get_pc()
        new_spsr_value = self.cpsr.value
        vect_offset = 16
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - 8), length=32)
        route_to_monitor = HaveSecurityExt() and self.scr.get_ea() and self.is_external_abort()
        take_to_hyp = HaveVirtExt() and HaveSecurityExt() and self.scr.get_ns() and self.cpsr.get_m() == "0b11010"
        route_to_hyp = (
            HaveVirtExt() and
            HaveSecurityExt() and
            not self.is_secure() and
            (
                self.second_stage_abort() or
                (
                    self.cpsr.get_m() != "0b11010" and
                    (self.is_external_abort() and self.is_async_abort() and self.hcr.get_amo()) or
                    (self.debug_exception() and self.hdcr.get_tde())
                ) or
                (
                    self.cpsr.get_m() == "0b10000" and
                    self.hcr.get_tge() and
                    (self.is_alignment_fault() or (self.is_external_abort() and not self.is_async_abort()))
                )
            )
        )
        if route_to_monitor:
            if self.cpsr.get_m() == "0b10110":
                self.scr.set_ns(False)
            self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif take_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if HaveSecurityExt() and self.cpsr.get_m() == "0b10110":
                self.scr.set_ns(False)
            self.cpsr.set_m("0b10111")
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.cpsr.set_i(True)
            if not HaveSecurityExt() or HaveVirtExt() or not self.scr.get_ns() or self.scr.get_aw():
                self.cpsr.set_a(True)
            self.cpsr.set_it(BitArray(length=8))
            self.cpsr.set_j(False)
            self.cpsr.set_t(self.sctlr.get_te())
            self.cpsr.set_e(self.sctlr.get_ee())
            self.branch_to(BitArray(uint=(self.exc_vector_base().uint + vect_offset), length=32))

    def increment_pc(self, opcode_length):
        self._R[self.RName.RName_PC] = bits_ops.add(self._R[self.RName.RName_PC], BitArray(bin=bin(opcode_length)), 32)

    def reset_control_registers(self):
        self.midr.value = BitArray(bin="01000001000011111010011101100000")
        self.sctlr.value = BitArray(bin="01000000000001010000000001111001")
        self.actlr = BitArray(bin="00000000000000000000000000000111")
        self.vbar.value = BitArray(bin=implementation_defined.vbar_bin)
