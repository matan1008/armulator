import bitstring
from bitstring import BitArray
from enum import Enum
from configurations import *
import shift
import bits_ops
import implementation_defined
from arm_exceptions import *
from memory_attributes import MemoryAttributes, MemType
from full_address import FullAddress
from address_descriptor import AddressDescriptor
from tlb_record import TLBRecord, TLBRecType
from memory import Memory
from permissions import Permissions
from enums import *
import opcodes
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


class CoreRegisters:
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
        self.CPSR = BitArray(length=32)
        self.SPSR_hyp = BitArray(length=32)
        self.SPSR_svc = BitArray(length=32)
        self.SPSR_abt = BitArray(length=32)
        self.SPSR_und = BitArray(length=32)
        self.SPSR_mon = BitArray(length=32)
        self.SPSR_irq = BitArray(length=32)
        self.SPSR_fiq = BitArray(length=32)
        self.ELR_hyp = BitArray(length=32)
        self.scr = SCR()
        self.nsacr = NSACR()
        self.sctlr = SCTLR()
        self.hstr = HSTR()
        self.hsr = HSR()
        self.hsctlr = HSCTLR()
        self.hvbar = BitArray(length=32)
        self.jmcr = JMCR()
        self.hcr = HCR()
        self.MVBAR = BitArray(length=32)
        self.TEEHBR = BitArray(length=32)
        self.hdcr = HDCR()
        self.vbar = VBAR()
        self.DBGDIDR = BitArray(length=32)
        self.DFSR = BitArray(length=32)
        self.DFAR = BitArray(length=32)
        self.HDFAR = BitArray(length=32)
        self.HPFAR = BitArray(length=32)
        self.ttbcr = TTBCR()
        self.fcseidr = FCSEIDR()
        self.htcr = HTCR()
        self.HTTBR = BitArray(length=64)
        self.TTBR0_64 = BitArray(length=64)
        self.TTBR1_64 = BitArray(length=64)
        self.VTCR = BitArray(length=32)
        self.vtcr = VTCR()
        self.VTTBR = BitArray(length=64)
        self.MAIR0 = BitArray(length=32)
        self.MAIR1 = BitArray(length=32)
        self.HMAIR0 = BitArray(length=32)
        self.HMAIR1 = BitArray(length=32)
        self.prrr = PRRR()
        self.nmrr = NMRR()
        self.dacr = DACR()
        self.mpuir = MPUIR()
        self.cpacr = CPACR()
        self.rgnr = RGNR(number_of_mpu_regions)
        self.hcptr = HCPTR()
        self.drsrs = [DRSR()] * number_of_mpu_regions
        self.DRBARs = [BitArray(length=32) for region in xrange(number_of_mpu_regions)]
        self.dracrs = [DRACR()] * number_of_mpu_regions
        self.IRBARs = [BitArray(length=32) for region in xrange(number_of_mpu_regions)]
        self.irsrs = [IRSR()] * number_of_mpu_regions
        self.iracrs = [IRACR()] * number_of_mpu_regions
        self.teecr = TEECR()
        self.event_register = False
        self.ELR_hyp = BitArray(length=32)
        self.midr = MIDR()
        self.CTR = BitArray(length=32)
        self.TCMTR = BitArray(length=32)
        self.TLBTR = BitArray(length=32)
        self.ID_PFR0 = BitArray(length=32)
        self.ID_PFR1 = BitArray(length=32)
        self.ID_DFR0 = BitArray(length=32)
        self.ID_AFR0 = BitArray(length=32)
        self.ID_MMFR0 = BitArray(length=32)
        self.ID_MMFR1 = BitArray(length=32)
        self.ID_MMFR2 = BitArray(length=32)
        self.ID_MMFR3 = BitArray(length=32)
        self.ID_ISAR0 = BitArray(length=32)
        self.ID_ISAR1 = BitArray(length=32)
        self.ID_ISAR2 = BitArray(length=32)
        self.ID_ISAR3 = BitArray(length=32)
        self.ID_ISAR4 = BitArray(length=32)
        self.ID_ISAR5 = BitArray(length=32)
        self.ACTLR = BitArray(length=32)
        self.sder = SDER()
        self.TTBR0 = BitArray(length=32)
        self.TTBR1 = BitArray(length=32)
        self.IFSR = BitArray(length=32)
        self.IFAR = BitArray(length=32)
        self.PAR = BitArray(length=32)
        self.CDSR = BitArray(length=32)
        self.DCLR = BitArray(length=32)
        self.ICLR = BitArray(length=32)
        self.DTCMRR = BitArray(length=32)
        self.DTCM_NSACR = BitArray(length=32)
        self.ITCM_NSACR = BitArray(length=32)
        self.TCMSR = BitArray(length=32)
        self.CBOR = BitArray(length=32)
        self.TLBLR = BitArray(length=32)
        self.DMAISPR = BitArray(length=32)
        self.DMAISQR = BitArray(length=32)
        self.DMAISRR = BitArray(length=32)
        self.DMAISIR = BitArray(length=32)
        self.DMAUAR = BitArray(length=32)
        self.DMACNR = BitArray(length=32)
        self.STOP_DMAER = BitArray(length=32)
        self.START_DMAER = BitArray(length=32)
        self.CLEAR_DMAER = BitArray(length=32)
        self.DMACR = BitArray(length=32)
        self.DMAISAR = BitArray(length=32)
        self.DMAESAR = BitArray(length=32)
        self.DMAIEAR = BitArray(length=32)
        self.DMACSR = BitArray(length=32)
        self.DMACIDR = BitArray(length=32)
        self.ISR = BitArray(length=32)
        self.CONTEXTIDR = BitArray(length=32)
        self.TPIDRURW = BitArray(length=32)
        self.TPIDRURO = BitArray(length=32)
        self.TPIDRPRW = BitArray(length=32)
        self.PPMRR = BitArray(length=32)
        self.sunavcr = SUNAVCR()
        self.pmcr = PMCR()
        self.CCR = BitArray(length=32)
        self.CR0 = BitArray(length=32)
        self.CR1 = BitArray(length=32)
        self.SVCR_RC = BitArray(length=32)
        self.SVCR_IC = BitArray(length=32)
        self.SVCR_FIC = BitArray(length=32)
        self.SVCR_EDRC = BitArray(length=32)
        self.SVCSMR = BitArray(length=32)
        self.fpexc = FPEXC()

    def coproc_register_name(self, coproc, crn, opc1, crm, opc2):
        if coproc == 15:
            if crn == 0:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "MIDR"
                        elif opc2 == 1:
                            return "CTR"
                        elif opc2 == 2:
                            return "TCMTR"
                        elif opc2 == 3:
                            return "TLBTR"
                    elif crm == 1:
                        if opc2 == 0:
                            return "ID_PFR0"
                        elif opc2 == 1:
                            return "ID_PFR1"
                        elif opc2 == 2:
                            return "ID_DFR0"
                        elif opc2 == 3:
                            return "ID_AFR0"
                        elif opc2 == 4:
                            return "ID_MMFR0"
                        elif opc2 == 5:
                            return "ID_MMFR1"
                        elif opc2 == 6:
                            return "ID_MMFR2"
                        elif opc2 == 7:
                            return "ID_MMFR3"
                    elif crm == 2:
                        if opc2 == 0:
                            return "ID_ISAR0"
                        elif opc2 == 1:
                            return "ID_ISAR1"
                        elif opc2 == 2:
                            return "ID_ISAR2"
                        elif opc2 == 3:
                            return "ID_ISAR3"
                        elif opc2 == 4:
                            return "ID_ISAR4"
                        elif opc2 == 5:
                            return "ID_ISAR5"
            elif crn == 1:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "SCTLR"
                        elif opc2 == 1:
                            return "ACTLR"
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
                            return "TTBR0"
                        elif opc2 == 1:
                            return "TTBR1"
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
                            return "IFSR"
            elif crn == 6:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "DFAR"
                        elif opc2 == 2:
                            return "IFAR"
            elif crn == 7:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 4:
                            return "CP15WFI"
                    elif crm == 4:
                        if opc2 == 0:
                            return "PAR"
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
                            return "CDSR"
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
                            return "DCLR"
                        elif opc2 == 0:
                            return "ICLR"
                    elif crm == 1:
                        if opc2 == 0:
                            return "DTCMRR"
                        elif opc2 == 1:
                            return "ITCMRR"
                        elif opc2 == 2:
                            return "DTCM_NSACR"
                        elif opc2 == 3:
                            return "ITCM_NSACR"
                    elif crm == 2:
                        if opc2 == 0:
                            return "TCMSR"
                    elif crm == 8:
                        if opc2 == 0:
                            return "CBOR"
            elif crn == 10:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "TLBLR"
                    elif crm == 2:
                        if opc2 == 0:
                            return "PRRR"
                        elif opc2 == 1:
                            return "NMRR"
            elif crn == 11:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "DMAISPR"
                        elif opc2 == 1:
                            return "DMAISQR"
                        elif opc2 == 2:
                            return "DMAISRR"
                        elif opc2 == 3:
                            return "DMAISIR"
                    elif crm == 1:
                        if opc2 == 0:
                            return "DMAUAR"
                    elif crm == 2:
                        if opc2 == 0:
                            return "DMACNR"
                    elif crm == 3:
                        if opc2 == 0:
                            return "STOP_DMAER"
                        elif opc2 == 1:
                            return "START_DMAER"
                        elif opc2 == 2:
                            return "CLEAR_DMAER"
                    elif crm == 4:
                        if opc2 == 0:
                            return "DMACR"
                    elif crm == 5:
                        if opc2 == 0:
                            return "DMAISAR"
                    elif crm == 6:
                        if opc2 == 0:
                            return "DMAESAR"
                    elif crm == 7:
                        if opc2 == 0:
                            return "DMAIEAR"
                    elif crm == 8:
                        if opc2 == 0:
                            return "DMACSR"
                    elif crm == 8:
                        if opc2 == 0:
                            return "DMACIDR"
            elif crn == 12:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "VBAR"
                        elif opc2 == 1:
                            return "MVBAR"
                    elif crm == 1:
                        if opc2 == 0:
                            return "ISR"
            elif crn == 13:
                if opc1 == 0:
                    if crm == 0:
                        if opc2 == 0:
                            return "FCSEIDR"
                        elif opc2 == 1:
                            return "CONTEXTIDR"
                        elif opc2 == 2:
                            return "TPIDRURW"
                        elif opc2 == 3:
                            return "TPIDRURO"
                        elif opc2 == 4:
                            return "TPIDRPRW"
            elif crn == 15:
                if opc1 == 0:
                    if crm == 2:
                        if opc2 == 4:
                            return "PPMRR"
                    elif crm == 9:
                        if opc2 == 0:
                            return "SUNAVCR"
                    elif crm == 12:
                        if opc2 == 0:
                            return "PMCR"
                        elif opc2 == 1:
                            return "CCR"
                        elif opc2 == 2:
                            return "CR0"
                        elif opc2 == 3:
                            return "CR1"
                        elif opc2 == 4:
                            return "SVCR_RC"
                        elif opc2 == 5:
                            return "SVCR_IC"
                        elif opc2 == 6:
                            return "SVCR_FIC"
                        elif opc2 == 7:
                            return "SVCR_EDRC"
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
                            return "SVCSMR"
                elif opc1 == 1:
                    if crm == 13:
                        # unknown
                        pass

    def get_cpsr_as_apsr(self):
        return self.CPSR & "0xF80F0000"

    def pc_store_value(self):
        # not sure
        return self._R[self.RName.RName_PC]

    def set_event_register(self, flag):
        self.event_register = flag

    def get_event_register(self):
        return self.event_register

    def get_dbgdidr_version(self):
        return self.DBGDIDR.bin[12:16]

    def get_cpsr_m(self):
        return self.CPSR.bin[27:32]

    def get_cpsr_n(self):
        return self.CPSR.bin[0]

    def get_cpsr_z(self):
        return self.CPSR.bin[1]

    def get_cpsr_c(self):
        return self.CPSR.bin[2]

    def get_cpsr_v(self):
        return self.CPSR.bin[3]

    def get_cpsr_e(self):
        return self.CPSR.bin[22]

    def get_cpsr_q(self):
        return self.CPSR.bin[4]

    def get_cpsr_j(self):
        return self.CPSR.bin[7]

    def get_cpsr_t(self):
        return self.CPSR.bin[26]

    def get_cpsr_isetstate(self):
        return self.CPSR.bin[7] + self.CPSR.bin[26]

    def get_cpsr_itstate(self):
        return self.CPSR.bin[16:22] + self.CPSR.bin[5:7]

    def get_cpsr_ge(self):
        return self.CPSR.bin[12:16]

    def set_dfar(self, new_dfar):
        self.DFAR = new_dfar

    def set_hdfar(self, new_hdfar):
        self.HDFAR = new_hdfar

    def set_hpfar(self, hpfar_28):
        self.HPFAR[0:28] = hpfar_28

    def set_dfsr(self, dfsr_14):
        self.DFAR[18:32] = dfsr_14

    def set_cpsr_ge(self, value):
        self.CPSR.overwrite(value, 12)

    def set_cpsr_m(self, value):
        self.CPSR.overwrite(value, 27)

    def set_cpsr_isetstate(self, state):
        self.CPSR[7] = state[0] == "1"
        self.CPSR[26] = state[1] == "1"

    def set_cpsr_n(self, flag):
        self.CPSR.set(int(flag), 0)

    def set_cpsr_z(self, flag):
        self.CPSR.set(int(flag), 1)

    def set_cpsr_c(self, flag):
        self.CPSR.set(int(flag), 2)

    def set_cpsr_v(self, flag):
        self.CPSR.set(int(flag), 3)

    def set_cpsr_q(self, flag):
        self.CPSR.set(int(flag), 4)

    def set_cpsr_j(self, flag):
        self.CPSR[7] = flag

    def set_cpsr_t(self, flag):
        self.CPSR[26] = flag

    def set_cpsr_e(self, flag):
        self.CPSR[22] = flag

    def set_cpsr_a(self, flag):
        self.CPSR[23] = flag

    def set_cpsr_i(self, flag):
        self.CPSR[24] = flag

    def set_cpsr_f(self, flag):
        self.CPSR[25] = flag

    def set_cpsr_itstate(self, state):
        self.CPSR.overwrite(state[0:6], 16)
        self.CPSR.overwrite(state[6:8], 5)

    def current_instr_set(self):
        isetstate = self.get_cpsr_isetstate()
        if isetstate == "00":
            result = InstrSet.InstrSet_ARM
        if isetstate == "01":
            result = InstrSet.InstrSet_Thumb
        if isetstate == "10":
            result = InstrSet.InstrSet_Jazelle
        if isetstate == "11":
            result = InstrSet.InstrSet_ThumbEE
        return result

    def select_instr_set(self, iset):
        if iset == InstrSet.InstrSet_ARM:
            if self.current_instr_set() == InstrSet.InstrSet_ThumbEE:
                print "unpredictable"
            else:
                self.set_cpsr_isetstate("00")
        if iset == InstrSet.InstrSet_Thumb:
            self.set_cpsr_isetstate("01")
        if iset == InstrSet.InstrSet_Jazelle:
            self.set_cpsr_isetstate("10")
        if iset == InstrSet.InstrSet_ThumbEE:
            self.set_cpsr_isetstate("11")

    def is_secure(self):
        return (not HaveSecurityExt()) or (not self.scr.get_ns()) or (self.get_cpsr_m() == "10110")

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
        if self.bad_mode(BitArray(bin=self.get_cpsr_m())):
            print "unpredictable"
        if self.get_cpsr_m() == "10000":
            return False
        return True

    def current_mode_is_hyp(self):
        if self.bad_mode(BitArray(bin=self.get_cpsr_m())):
            print "unpredictable"
        if self.get_cpsr_m() == "11010":
            return True
        return False

    def current_mode_is_user_or_system(self):
        if self.bad_mode(BitArray(bin=self.get_cpsr_m())):
            print "unpredictable"
        if self.get_cpsr_m() == "10000":
            return True
        if self.get_cpsr_m() == "11111":
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
            result = self.get_rmode(n, BitArray(bin=self.get_cpsr_m()))
        return result

    def set(self, n, value):
        assert 0 <= n <= 14
        self.changed_registers[n] = True
        self.set_rmode(n, BitArray(bin=self.get_cpsr_m()), value)

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
        if self.bad_mode(BitArray(bin=self.get_cpsr_m())):
            print "unpredictable"
            result = BitArray(length=32)
        else:
            result = BitArray(length=32)
            if self.get_cpsr_m() == "10001":
                result = self.SPSR_fiq
            elif self.get_cpsr_m() == "10010":
                result = self.SPSR_irq
            elif self.get_cpsr_m() == "10011":
                result = self.SPSR_svc
            elif self.get_cpsr_m() == "10110":
                result = self.SPSR_mon
            elif self.get_cpsr_m() == "10111":
                result = self.SPSR_abt
            elif self.get_cpsr_m() == "11010":
                result = self.SPSR_hyp
            elif self.get_cpsr_m() == "11011":
                result = self.SPSR_und
            else:
                print "unpredictable"
        return result

    def set_spsr(self, value):
        if self.bad_mode(BitArray(bin=self.get_cpsr_m())):
            print "unpredictable"
        else:
            if self.get_cpsr_m() == "10001":
                self.SPSR_fiq = value
            elif self.get_cpsr_m() == "10010":
                self.SPSR_irq = value
            elif self.get_cpsr_m() == "10011":
                self.SPSR_svc = value
            elif self.get_cpsr_m() == "10110":
                self.SPSR_mon = value
            elif self.get_cpsr_m() == "10111":
                self.SPSR_abt = value
            elif self.get_cpsr_m() == "11010":
                self.SPSR_hyp = value
            elif self.get_cpsr_m() == "11011":
                self.SPSR_und = value
            else:
                print "unpredictable"

    def it_advance(self):
        if self.get_cpsr_itstate()[-3:] == "000":
            self.set_cpsr_itstate(BitArray(bin="00000000"))
        else:
            itstate = BitArray(bin=self.get_cpsr_itstate())
            itstate.overwrite(shift.lsl(itstate[4:], 1), 4)

    def cpsr_write_by_instr(self, value, bytemask, is_excp_return):
        privileged = self.current_mode_is_not_user()
        nmfi = self.sctlr.get_nmfi()
        if bytemask[0]:
            self.CPSR.overwrite(value[0:5], 0)
            if is_excp_return:
                self.CPSR.overwrite(value[5:8], 5)
        if bytemask[1]:
            self.CPSR.overwrite(value[12:16], 12)
        if bytemask[2]:
            if is_excp_return:
                self.CPSR.overwrite(value[16:22], 16)
            self.CPSR.set(value[22], 22)
            if privileged and (self.is_secure() or self.scr.get_aw() or HaveVirtExt()):
                self.CPSR.set(value[23], 23)
        if bytemask[3]:
            if privileged:
                self.CPSR.set(value[24], 24)
            if privileged and (not nmfi or not value[25]) and (self.is_secure() or self.scr.get_fw() or HaveVirtExt()):
                self.CPSR.set(value[25], 25)
            if is_excp_return:
                self.CPSR.set(value[26], 26)
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
                    elif not self.is_secure() and self.get_cpsr_m() != "11010" and value.bin[27:] == "11010":
                        print "unpredictable"
                    elif self.get_cpsr_m() == "11010" and value.bin[27:] != "11010" and not is_excp_return:
                        print "unpredictable"
                    else:
                        self.CPSR.overwrite(value[27:], 27)

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
        self.set_cpsr_m(BitArray(bin="11010"))
        self.set_spsr(new_spsr_value)
        self.ELR_hyp = preferred_exceptn_return
        self.set_cpsr_j(False)
        self.set_cpsr_t(self.hsctlr.get_te())
        self.set_cpsr_e(self.hsctlr.get_ee())
        if not self.scr.get_ea():
            self.set_cpsr_a(True)
        if not self.scr.get_fiq():
            self.set_cpsr_f(True)
        if not self.scr.get_irq():
            self.set_cpsr_i(True)
        self.set_cpsr_itstate(BitArray(length=8))
        self.branch_to(BitArray(uint=(self.hvbar.uint + vect_offset), length=32))

    def enter_monitor_mode(self, new_spsr_value, new_lr_value, vect_offset):
        self.set_cpsr_m("0b10110")
        self.set_spsr(new_spsr_value)
        self.set(14, new_lr_value)
        self.set_cpsr_j(False)
        self.set_cpsr_t(self.sctlr.get_te())
        self.set_cpsr_e(self.sctlr.get_ee())
        self.set_cpsr_a(True)
        self.set_cpsr_f(True)
        self.set_cpsr_i(True)
        self.set_cpsr_itstate(BitArray(length=8))
        self.branch_to(BitArray(uint=(self.MVBAR.uint + vect_offset), length=32))

    def take_hyp_trap_exception(self):
        preferred_exceptn_return = BitArray(
            uint=(self.get_pc().uint - 4 if self.get_cpsr_t() == "1" else self.get_pc().uint - 8), length=32)
        new_spsr_value = self.CPSR
        self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)

    def take_smc_exception(self):
        self.it_advance()
        new_lr_value = self.get_pc() if self.get_cpsr_t() == "1" else BitArray(uint=(self.get_pc().uint - 4), length=32)
        new_spsr_value = self.CPSR
        vect_offset = 8
        if self.get_cpsr_m() == "10110":
            self.scr.set_ns(False)
        self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)

    def take_data_abort_exception(self):
        new_lr_value = BitArray(uint=self.get_pc().uint + 4, length=32) if self.get_cpsr_t() == "1" else self.get_pc()
        new_spsr_value = self.CPSR
        vect_offset = 16
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - 8), length=32)
        route_to_monitor = HaveSecurityExt() and self.scr.get_ea() and self.is_external_abort()
        take_to_hyp = HaveVirtExt() and HaveSecurityExt() and self.scr.get_ns() and self.get_cpsr_m() == "11010"
        route_to_hyp = (
            HaveVirtExt() and
            HaveSecurityExt() and
            not self.is_secure() and
            (
                self.second_stage_abort() or
                (
                    self.get_cpsr_m() != "11010" and
                    (self.is_external_abort() and self.is_async_abort() and self.hcr.get_amo()) or
                    (self.debug_exception() and self.hdcr.get_tde())
                ) or
                (
                    self.get_cpsr_m() == "10000" and
                    self.hcr.get_tge() and
                    (self.is_alignment_fault() or (self.is_external_abort() and not self.is_async_abort()))
                )
            )
        )
        if route_to_monitor:
            if self.get_cpsr_m() == "10110":
                self.scr.set_ns(False)
            self.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif take_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if HaveSecurityExt() and self.get_cpsr_m() == "10110":
                self.scr.set_ns(False)
            self.set_cpsr_m("0b10111")
            self.set_spsr(new_spsr_value)
            self.set(14, new_lr_value)
            self.set_cpsr_i(True)
            if not HaveSecurityExt() or HaveVirtExt() or not self.scr.get_ns() or self.scr.get_aw():
                self.set_cpsr_a(True)
            self.set_cpsr_itstate(BitArray(length=8))
            self.set_cpsr_j(False)
            self.set_cpsr_t(self.sctlr.get_te())
            self.set_cpsr_e(self.sctlr.get_ee())
            self.branch_to(BitArray(uint=(self.exc_vector_base().uint + vect_offset), length=32))

    def increment_pc(self, opcode_length):
        self._R[self.RName.RName_PC] = bits_ops.add(self._R[self.RName.RName_PC], BitArray(bin=bin(opcode_length)), 32)
        # if self.current_instr_set() == self.InstrSet.InstrSet_ARM:
        #    self._R[self.RName.RName_PC] = BitsOps.add(self._R[self.RName.RName_PC], BitArray(bin="100"), 32)
        # elif self.current_instr_set() == self.InstrSet.InstrSet_Thumb:
        #    self._R[self.RName.RName_PC] = BitsOps.add(self._R[self.RName.RName_PC], BitArray(bin="10"), 32)

    def reset_control_registers(self):
        self.midr.value = BitArray(bin="01000001000011111010011101100000")
        self.sctlr.value = BitArray(bin="01000000000001010000000001111001")
        self.ACTLR = BitArray(bin="00000000000000000000000000000111")
        self.vbar.value = BitArray(bin=implementation_defined.vbar_bin)


class ARM1176:
    def __init__(self):
        self.core_registers = CoreRegisters()
        self.run = True
        self.opcode = BitArray(length=32)
        dabort = ("DAbort_AccessFlag DAbort_Alignment DAbort_Background DAbort_Domain DAbort_Permission "
                  "DAbort_Translation DAbort_SyncExternal DAbort_SyncExternalonWalk DAbort_SyncParity "
                  "DAbort_SyncParityonWalk DAbort_AsyncParity DAbort_AsyncExternal DAbort_SyncWatchpoint "
                  "DAbort_AsyncWatchpoint DAbort_TLBConflict DAbort_Lockdown DAbort_Coproc DAbort_ICacheMaint ")
        self.DAbort = Enum("DAbort", dabort)
        self.mem = Memory()
        self.is_wait_for_event = False
        self.is_wait_for_interrupt = False
        self.__init_registers__()

    def __init_registers__(self):
        # self.take_reset()
        pass

    def start(self):
        self.take_reset()

    def print_core_registers(self):
        print "{0}:{1}".format("R0", self.core_registers.get(0))
        print "{0}:{1}".format("R1", self.core_registers.get(1))
        print "{0}:{1}".format("R2", self.core_registers.get(2))
        print "{0}:{1}".format("R3", self.core_registers.get(3))
        print "{0}:{1}".format("R4", self.core_registers.get(4))
        print "{0}:{1}".format("R5", self.core_registers.get(5))
        print "{0}:{1}".format("R6", self.core_registers.get(6))
        print "{0}:{1}".format("R7", self.core_registers.get(7))
        print "{0}:{1}".format("R8", self.core_registers.get(8))
        print "{0}:{1}".format("R9", self.core_registers.get(9))
        print "{0}:{1}".format("R10", self.core_registers.get(10))
        print "{0}:{1}".format("R11", self.core_registers.get(11))
        print "{0}:{1}".format("R12", self.core_registers.get(12))
        print "{0}:{1}".format("SP", self.core_registers.get_sp())
        print "{0}:{1}".format("LR", self.core_registers.get_lr())
        print "{0}:{1}".format("PC", self.core_registers.pc_store_value())
        print "{0}:{1}".format("CPSR", self.core_registers.CPSR)
        # print "{0}:{1}".format(, self.core_registers.)
        # print "{0}:{1}".format(, self.core_registers.)

    def take_reset(self):
        self.core_registers.set_cpsr_m("0b10011")
        if HaveSecurityExt():
            self.core_registers.scr.set_ns(False)
        self.core_registers.reset_control_registers()
        if HaveAdvSIMDorVFP():
            self.core_registers.fpexc.set_en(False)
        if HaveThumbEE():
            self.core_registers.teecr.set_xed(False)
        if HaveJazelle():
            self.core_registers.jmcr.set_je(False)
        self.core_registers.set_cpsr_i(True)
        self.core_registers.set_cpsr_f(True)
        self.core_registers.set_cpsr_a(True)
        self.core_registers.set_cpsr_itstate(BitArray(length=8))
        self.core_registers.set_cpsr_j(False)
        self.core_registers.set_cpsr_t(self.core_registers.sctlr.get_te())
        self.core_registers.set_cpsr_e(self.core_registers.sctlr.get_ee())
        reset_vector = (implementation_defined.impdef_reset_vector
                        if HasIMPDEFResetVactor()
                        else self.core_registers.exc_vector_base())
        reset_vector[31] = False
        self.core_registers.branch_to(reset_vector)

    def take_hyp_trap_exception(self):
        preferred_exceptn_return = BitArray(uint=(self.core_registers.get_pc().uint - 4
                                                  if self.core_registers.get_cpsr_t() == "1"
                                                  else self.core_registers.get_pc().uint - 8),
                                            length=32)
        new_spsr_value = self.core_registers.CPSR
        self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)

    def take_smc_exception(self):
        self.core_registers.it_advance()
        new_lr_value = self.core_registers.get_pc() if self.core_registers.get_cpsr_t() == "1" else BitArray(
            uint=(self.core_registers.get_pc().uint - 4), length=32)
        new_spsr_value = self.core_registers.CPSR
        vect_offset = 8
        if self.core_registers.get_cpsr_m() == "10110":
            self.core_registers.scr.set_ns(False)
        self.core_registers.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)

    def take_data_abort_exception(self):
        new_lr_value = BitArray(uint=self.core_registers.get_pc().uint + 4,
                                length=32) if self.core_registers.get_cpsr_t() == "1" else self.core_registers.get_pc()
        new_spsr_value = self.core_registers.CPSR
        vect_offset = 16
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - 8), length=32)
        route_to_monitor = (HaveSecurityExt() and
                            self.core_registers.scr.get_ea() and
                            self.core_registers.is_external_abort())
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.core_registers.scr.get_ns() and
                       self.core_registers.get_cpsr_m() == "11010")
        route_to_hyp = (
            HaveVirtExt() and
            HaveSecurityExt() and
            not self.core_registers.is_secure() and
            (
                self.core_registers.second_stage_abort() or
                (
                    self.core_registers.get_cpsr_m() != "11010" and
                    (
                        self.core_registers.is_external_abort() and
                        self.core_registers.is_async_abort() and
                        self.core_registers.hcr.get_amo()
                    ) or
                    (
                        self.core_registers.debug_exception() and
                        self.core_registers.hdcr.get_tde()
                    )
                ) or
                (
                    self.core_registers.get_cpsr_m() == "10000" and
                    self.core_registers.hcr.get_tge() and
                    (
                        self.core_registers.is_alignment_fault() or
                        (
                            self.core_registers.is_external_abort() and
                            not self.core_registers.is_async_abort()
                        )
                    )
                )
            )
        )
        if route_to_monitor:
            if self.core_registers.get_cpsr_m() == "10110":
                self.core_registers.scr.set_ns(False)
            self.core_registers.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif take_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if HaveSecurityExt() and self.core_registers.get_cpsr_m() == "10110":
                self.core_registers.scr.set_ns(False)
            self.core_registers.set_cpsr_m("0b10111")
            self.core_registers.set_spsr(new_spsr_value)
            self.core_registers.set(14, new_lr_value)
            self.core_registers.set_cpsr_i(True)
            if (not HaveSecurityExt() or
                    HaveVirtExt() or
                    not self.core_registers.scr.get_ns() or
                    self.core_registers.scr.get_aw()):
                self.core_registers.set_cpsr_a(True)
            self.core_registers.set_cpsr_itstate(BitArray(length=8))
            self.core_registers.set_cpsr_j(False)
            self.core_registers.set_cpsr_t(self.core_registers.sctlr.get_te())
            self.core_registers.set_cpsr_e(self.core_registers.sctlr.get_ee())
            self.core_registers.branch_to(
                BitArray(uint=(self.core_registers.exc_vector_base().uint + vect_offset), length=32))

    def take_svc_exception(self):
        self.core_registers.it_advance()
        new_lr_value = bits_ops.sub(self.core_registers.get_pc(), BitArray(bin="10"),
                                    32) if self.core_registers.get_cpsr_t() == "1" else bits_ops.sub(
            self.core_registers.get_pc(), BitArray(bin="100"), 32)
        new_spsr_value = self.core_registers.CPSR
        vect_offset = 8
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.core_registers.scr.get_ns() and
                       self.core_registers.get_cpsr_m() == "11010")
        route_to_hyp = (HaveVirtExt() and
                        HaveSecurityExt() and
                        not self.core_registers.is_secure() and
                        self.core_registers.hcr.get_tge() and
                        self.core_registers.get_cpsr_m() == "10000")
        preferred_exceptn_return = new_lr_value
        if take_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.core_registers.get_cpsr_m() == "10110":
                self.core_registers.scr.set_ns(False)
            self.core_registers.set_cpsr_m("0b10011")
            self.core_registers.set_spsr(new_spsr_value)
            self.core_registers.set(14, new_lr_value)
            self.core_registers.set_cpsr_i(True)
            self.core_registers.set_cpsr_itstate(BitArray(length=8))
            self.core_registers.set_cpsr_j(False)
            self.core_registers.set_cpsr_t(self.core_registers.sctlr.get_te())
            self.core_registers.set_cpsr_e(self.core_registers.sctlr.get_ee())
            self.core_registers.branch_to(
                bits_ops.add(self.core_registers.exc_vector_base(), BitArray(uint=vect_offset, length=32), 32))

    def take_undef_instr_exception(self):
        new_lr_value = BitArray(uint=(self.core_registers.get_pc().uint - 2),
                                length=32) if self.core_registers.get_cpsr_t() == "1" else BitArray(
            uint=(self.core_registers.get_pc().uint - 4), length=32)
        new_spsr_value = self.core_registers.CPSR
        vect_offset = 4
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.core_registers.scr.get_ns() and
                       self.core_registers.get_cpsr_m() == "11010")
        route_to_hyp = (HaveVirtExt() and
                        HaveSecurityExt() and
                        not self.core_registers.is_secure() and
                        self.core_registers.hcr.get_tge() and
                        self.core_registers.get_cpsr_m() == "10000")
        return_offset = 2 if self.core_registers.get_cpsr_t() == "1" else 4
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - return_offset), length=32)
        if take_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.core_registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.core_registers.get_cpsr_m() == "10110":
                self.core_registers.scr.set_ns(False)
            self.core_registers.set_cpsr_m("0b11011")
            self.core_registers.set_spsr(new_spsr_value)
            self.core_registers.set(14, new_lr_value)
            self.core_registers.set_cpsr_i(True)
            self.core_registers.set_cpsr_itstate(BitArray(length=8))
            self.core_registers.set_cpsr_j(False)
            self.core_registers.set_cpsr_t(self.core_registers.sctlr.get_te())
            self.core_registers.set_cpsr_e(self.core_registers.sctlr.get_ee())
            self.core_registers.branch_to(
                BitArray(uint=(self.core_registers.exc_vector_base().uint + vect_offset), length=32))

    def big_endian_reverse(self, value, n):
        assert n == 1 or n == 2 or n == 4 or n == 8
        if n == 1:
            result = value
        elif n == 2:
            result = value[8:16] + value[0:8]
        elif n == 4:
            result = value[24:32] + value[16:24] + value[8:16] + value[0:8]
        elif n == 8:
            result = (value[56:64] +
                      value[48:56] +
                      value[40:48] +
                      value[32:40] +
                      value[24:32] +
                      value[16:24] +
                      value[8:16] +
                      value[0:8])
        return result

    def encode_ldfsr(self, dtype, level):
        result = BitArray(length=6)
        if dtype == self.DAbort.DAbort_AccessFlag:
            result[0:4] = "0b0010"
            result[4:] = bin(level & 3)
        elif dtype == self.DAbort.DAbort_Alignment:
            result[0:6] = "0b100001"
        elif dtype == self.DAbort.DAbort_Permission:
            result[0:4] = "0b0011"
            result[4:] = bin(level & 3)
        elif dtype == self.DAbort.DAbort_Translation:
            result[0:4] = "0b0001"
            result[4:] = bin(level & 3)
        elif dtype == self.DAbort.DAbort_SyncExternal:
            result[0:6] = "0b100000"
        elif dtype == self.DAbort.DAbort_SyncExternalonWalk:
            result[0:4] = "0b0101"
            result[4:] = bin(level & 3)
        elif dtype == self.DAbort.DAbort_SyncParity:
            result[0:6] = "0b011000"
        elif dtype == self.DAbort.DAbort_SyncParityonWalk:
            result[0:4] = "0b0111"
            result[4:] = bin(level & 3)
        elif dtype == self.DAbort.DAbort_AsyncParity:
            result[0:6] = "0b011001"
        elif dtype == self.DAbort.DAbort_AsyncExternal:
            result[0:6] = "0b010001"
        elif dtype == self.DAbort.DAbort_SyncWatchpoint or dtype == self.DAbort.DAbort_AsyncWatchpoint:
            result[0:6] = "0b100010"
        elif dtype == self.DAbort.DAbort_TLBConflict:
            result[0:6] = "0b110000"
        elif dtype == self.DAbort.DAbort_Lockdown:
            result[0:6] = "0b110100"
        elif dtype == self.DAbort.DAbort_Coproc:
            result[0:6] = "0b111010"
        else:
            pass  # unknown
        return result

    def encode_sdfsr(self, dtype, level):
        result = BitArray(length=5)
        if dtype == self.DAbort.DAbort_AccessFlag:
            if level == 1:
                result[0:5] = "0b00011"
            else:
                result[0:5] = "0b00110"
        elif dtype == self.DAbort.DAbort_Alignment:
            result[0:5] = "0b00001"
        elif dtype == self.DAbort.DAbort_Permission:
            result[0:3] = "0b010"
            result[4] = True
            result[3] = (level >> 1) & 1
        elif dtype == self.DAbort.DAbort_Translation:
            result[0:3] = "0b001"
            result[4] = True
            result[3] = (level >> 1) & 1
        elif dtype == self.DAbort.DAbort_SyncExternal:
            result[0:5] = "0b01000"
        elif dtype == self.DAbort.DAbort_SyncExternalonWalk:
            result[0:3] = "0b011"
            result[4] = False
            result[3] = (level >> 1) & 1
        elif dtype == self.DAbort.DAbort_SyncParity:
            result[0:5] = "0b11001"
        elif dtype == self.DAbort.DAbort_SyncParityonWalk:
            result[0:3] = "0b111"
            result[4] = False
            result[3] = (level >> 1) & 1
        elif dtype == self.DAbort.DAbort_AsyncParity:
            result[0:5] = "0b11000"
        elif dtype == self.DAbort.DAbort_AsyncExternal:
            result[0:5] = "0b10110"
        elif dtype == self.DAbort.DAbort_SyncWatchpoint or dtype == self.DAbort.DAbort_AsyncWatchpoint:
            result[0:5] = "0b00010"
        elif dtype == self.DAbort.DAbort_TLBConflict:
            result[0:5] = "0b10000"
        elif dtype == self.DAbort.DAbort_Lockdown:
            result[0:5] = "0b10100"
        elif dtype == self.DAbort.DAbort_Coproc:
            result[0:5] = "0b11010"
        elif dtype == self.DAbort.DAbort_ICacheMaint:
            result[0:5] = "0b00100"
        else:
            pass  # unknown
        return result

    def encode_pmsafsr(self, dtype, level):
        result = BitArray(length=5)
        if dtype == self.DAbort.DAbort_Alignment:
            result[0:5] = "0b00001"
        elif dtype == self.DAbort.DAbort_Permission:
            result[0:5] = "0b01101"
        elif dtype == self.DAbort.DAbort_SyncExternal:
            result[0:5] = "0b01000"
        elif dtype == self.DAbort.DAbort_SyncParity:
            result[0:5] = "0b11001"
        elif dtype == self.DAbort.DAbort_AsyncParity:
            result[0:5] = "0b11000"
        elif dtype == self.DAbort.DAbort_AsyncExternal:
            result[0:5] = "0b10110"
        elif dtype == self.DAbort.DAbort_SyncWatchpoint or dtype == self.DAbort.DAbort_AsyncWatchpoint:
            result[0:5] = "0b00010"
        elif dtype == self.DAbort.DAbort_Background:
            result[0:5] = "0b00000"
        elif dtype == self.DAbort.DAbort_Lockdown:
            result[0:5] = "0b10100"
        elif dtype == self.DAbort.DAbort_Coproc:
            result[0:5] = "0b11010"
        else:
            pass  # unknown
        return result

    def current_cond(self):
        if self.core_registers.current_instr_set() == InstrSet.InstrSet_ARM:
            result = self.opcode[0:4]
        elif self.opcode.length == 16 and self.opcode.bin[0:4] == "1101":
            result = self.opcode[4:8]
        elif self.opcode.length == 32 and self.opcode.bin[0:5] == "11110" and self.opcode.bin[16:18] == "10" and not \
                self.opcode[19]:
            result = self.opcode[6:10]
        else:
            if self.core_registers.get_cpsr_itstate()[4:8] != "0000":
                result = BitArray(bin=self.core_registers.get_cpsr_itstate()[0:4])
            elif self.core_registers.get_cpsr_itstate() == "00000000":
                result = BitArray(bin="1110")
            else:
                print "unpredictable"
        return result

    def condition_passed(self):
        cond = self.current_cond()
        if cond.bin[0:3] == "000":
            result = self.core_registers.get_cpsr_z() == "1"
        elif cond.bin[0:3] == "001":
            result = self.core_registers.get_cpsr_c() == "1"
        elif cond.bin[0:3] == "010":
            result = self.core_registers.get_cpsr_n() == "1"
        elif cond.bin[0:3] == "011":
            result = self.core_registers.get_cpsr_v() == "1"
        elif cond.bin[0:3] == "100":
            result = self.core_registers.get_cpsr_c() == "1" and self.core_registers.get_cpsr_z() == "0"
        elif cond.bin[0:3] == "101":
            result = self.core_registers.get_cpsr_n() == self.core_registers.get_cpsr_v()
        elif cond.bin[0:3] == "110":
            result = (self.core_registers.get_cpsr_n() == self.core_registers.get_cpsr_v() and
                      self.core_registers.get_cpsr_z() == "0")
        elif cond.bin[0:3] == "111":
            result = True
        if cond[3] and cond.bin != "1111":
            result = not result
        return result

    def this_instr_length(self):
        return self.opcode.len

    def this_instr(self):
        return self.opcode

    def write_hsr(self, ec, hsr_string):
        hsr_value = bits_ops.zeros(32)
        hsr_value[0:6] = ec
        if (ec.uint in (0x0, 0x20, 0x21)) or (ec.uint in (0x24, 0x25) and hsr_string[7]):
            hsr_value[6] = 1 if self.this_instr_length() == 32 else 0
        if ec.bin[0:2] == "00" and ec.bin[2:6] != "0000":
            if self.core_registers.current_instr_set() == InstrSet.InstrSet_ARM:
                hsr_value[7] = True
                hsr_value[8:12] = self.current_cond()
            else:
                hsr_value[7] = implementation_defined.write_hsr_hsr_value_24
                if hsr_value[7]:
                    if self.condition_passed():
                        hsr_value[8:12] = (self.current_cond()
                                           if implementation_defined.write_hsr_23_22_cond
                                           else BitArray(bin="1110"))
                    else:
                        hsr_value[8:12] = self.current_cond()
            hsr_value[12:] = hsr_string[12:]
        else:
            hsr_value[7:] = hsr_string
        self.core_registers.hsr.value = hsr_value

    def switch_to_jazelle_execution(self):
        raise NotImplementedError()

    def branch_write_pc(self, address):
        if self.core_registers.current_instr_set() == InstrSet.InstrSet_ARM:
            if ArchVersion() < 6 and address.bin[29:] != "00":
                print "unpredictable"
            self.core_registers.branch_to(address[:-2] + BitArray(bin="00"))
        elif self.core_registers.current_instr_set() == InstrSet.InstrSet_Jazelle:
            if JazelleAcceptsExecution():
                self.core_registers.branch_to(address)
            else:
                self.core_registers.branch_to(address[:-2] + BitArray(bin="00"))
        else:
            address.set(False, 31)
            self.core_registers.branch_to(address)

    def bx_write_pc(self, address):
        if self.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE:
            if address[31]:
                address.set(False, 31)
                self.core_registers.branch_to(address)
            else:
                print "unpredictable"
        else:
            if address[31]:
                self.core_registers.select_instr_set(InstrSet.InstrSet_Thumb)
                address.set(False, 31)
                self.core_registers.branch_to(address)
            elif not address[30]:
                self.core_registers.select_instr_set(InstrSet.InstrSet_ARM)
                self.core_registers.branch_to(address)
            else:
                print "unpredictable"

    def alu_write_pc(self, address):
        if ArchVersion() >= 7 and self.core_registers.current_instr_set() == InstrSet.InstrSet_ARM:
            self.bx_write_pc(address)
        else:
            self.branch_write_pc(address)

    def load_write_pc(self, address):
        if ArchVersion() >= 5:
            self.bx_write_pc(address)
        else:
            self.branch_write_pc(address)

    def tlb_lookup_came_from_cache_maintenance(self):
        # mock
        raise NotImplementedError()

    def ls_instruction_syndrome(self):
        # mock
        raise NotImplementedError()

    def null_check_if_thumbee(self, n):
        if self.core_registers.current_instr_set() == InstrSet.InstrSet_ThumbEE:
            if n == 15:
                if bits_ops.align(self.core_registers.get_pc(), 4).all(False):
                    print "unpredictable"
            elif n == 13:
                if self.core_registers.get_sp().all(False):
                    print "unpredictable"
            else:
                if self.core_registers.get(n).all(False):
                    self.core_registers.set_lr(self.core_registers.get_pc()[:-1] + BitArray(bin="1"))
                    self.core_registers.set_cpsr_itstate(BitArray(bin="00000000"))
                    self.branch_write_pc(BitArray(uint=(self.core_registers.TEEHBR.uint - 4), length=32))
                    raise EndOfInstruction("NullCheckIfThumbEE")

    def fcse_translate(self, va):
        if va.bin[0:7] == "0000000":
            mva = self.core_registers.fcseidr.get_pid() + va[7:32]
        else:
            mva = va
        return mva

    def default_memory_attributes(self, va):
        memattrs = MemoryAttributes()
        if va[0:2] == "0b00":
            if not self.core_registers.sctlr.get_c():
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b00"
                memattrs.shareable = True
            else:
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b01"
                memattrs.shareable = False
        elif va[0:2] == "0b01":
            if not self.core_registers.sctlr.get_c() or va[2]:
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b00"
                memattrs.shareable = True
            else:
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b10"
                memattrs.shareable = False
        elif va[0:2] == "0b10":
            memattrs.type = MemType.MemType_Device
            memattrs.innerattrs[0:2] = "0b00"
            memattrs.shareable = va[2]
        elif va[0:2] == "0b11":
            memattrs.type = MemType.MemType_StronglyOrdered
            memattrs.innerattrs[0:2] = "0b00"
            memattrs.shareable = True
        memattrs.outerattrs = memattrs.innerattrs
        memattrs.outershareable = memattrs.shareable
        return memattrs

    def convert_attrs_hints(self, rgn):
        attributes = BitArray(length=2)
        hints = BitArray(length=2)
        if rgn.uint == 0:
            attributes[0:2] = "0b00"
            hints[0:2] = "0b00"
        elif rgn[1]:
            attributes[0:2] = "0b11"
            hints[0] = True
            hints[1] = not rgn[0]
        else:
            attributes[0:2] = "0b10"
            hints[0:2] = "0b10"
        return hints + attributes

    def check_permission(self, perms, mva, level, domain, iswrite, ispriv, taketohypmode, ldfsr_format):
        secondstageabort = False
        ipavalid = False
        s2fs1walk = False
        ipa = BitArray(length=40)  # unknown
        if self.core_registers.sctlr.get_afe():
            perms.ap[2] = True
        abort = False
        if perms.ap == "0b000":
            abort = True
        elif perms.ap == "0b001":
            abort = not ispriv
        elif perms.ap == "0b010":
            abort = not ispriv and iswrite
        elif perms.ap == "0b011":
            abort = False
        elif perms.ap == "0b100":
            print "unpredictable"
        elif perms.ap == "0b101":
            abort = not ispriv or iswrite
        elif perms.ap == "0b110":
            abort = iswrite
        elif perms.ap == "0b111":
            if MemorySystemArchitecture() == MemArch.MemArch_VMSA:
                abort = iswrite
            else:
                print "unpredictable"
        if abort:
            self.data_abort(mva, ipa, domain, level, iswrite, self.DAbort.DAbort_Permission, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)

    def check_permission_s2(self, perms, mva, ipa, level, iswrite, s2fs1walk):
        abort = (iswrite and not perms[2]) or (not iswrite and not perms[1])
        if abort:
            domain = BitArray(length=4)  # unknown
            taketohypmode = True
            secondstageabort = True
            ipavalid = s2fs1walk
            ldfsr_format = True
            self.data_abort(mva, ipa, domain, level, iswrite, self.DAbort.DAbort_Permission, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)

    def check_domain(self, domain, mva, level, iswrite):
        ipaddress = BitArray(length=40)  # unknown
        taketohypmode = False
        secondstageabort = False
        ipavalid = False
        ldfsr_format = False
        s2fs1walk = False
        permission_check = False
        if self.core_registers.dacr.get_d_n(domain.uint) == "0b00":
            self.data_abort(mva, ipaddress, domain, level, iswrite, self.DAbort.DAbort_Domain, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
        elif self.core_registers.dacr.get_d_n(domain.uint) == "0b01":
            permission_check = True
        if self.core_registers.dacr.get_d_n(domain.uint) == "0b10":
            print "unpredictable"
        if self.core_registers.dacr.get_d_n(domain.uint) == "0b11":
            permission_check = False
        return permission_check

    def second_stage_translate(self, s1_out_addr_desc, mva, size, is_write):
        result = AddressDescriptor()
        tlbrecord_s2 = TLBRecord()
        if HaveVirtExt() and not self.core_registers.is_secure() and not self.core_registers.current_mode_is_hyp():
            if self.core_registers.hcr.get_vm():
                s2ia = s1_out_addr_desc.paddress.physicaladdress
                stage1 = False
                s2fs1walk = True
                tlbrecord_s2 = self.translation_table_walk_ld(s2ia, mva, is_write, stage1, s2fs1walk, size)
                self.check_permission_s2(tlbrecord_s2.perms, mva, s2ia, tlbrecord_s2.level, False, s2fs1walk)
                if self.core_registers.hcr.get_ptw():
                    if tlbrecord_s2.addrdesc.memattrs.type != MemType.MemType_Normal:
                        domain = BitArray(length=4)  # unknown
                        taketohypmode = True
                        secondstageabort = True
                        ipavalid = True
                        ldfsr_format = True
                        s2fs1walk = True
                        self.data_abort(mva, s2ia, domain, tlbrecord_s2.level, is_write, self.DAbort.DAbort_Permission,
                                        taketohypmode, secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
                result = self.combine_s1s2_desc(s1_out_addr_desc, tlbrecord_s2.addrdesc)
            else:
                result = s1_out_addr_desc
        return result

    def data_abort(self, vaddress, ipaddress, domain, level, iswrite, dtype, taketohypmode, secondstageabort, ipavalid,
                   ldfsr_format, s2fs1walk):
        if MemorySystemArchitecture() == MemArch.MemArch_VMSA:
            if not taketohypmode:
                dfsr_string = BitArray(length=14)
                if dtype in (self.DAbort.DAbort_AsyncParity, self.DAbort.DAbort_AsyncExternal,
                             self.DAbort.DAbort_AsyncWatchpoint) or (dtype == self.DAbort.DAbort_SyncWatchpoint and int(
                        self.core_registers.get_dbgdidr_version()) <= 4):
                    self.core_registers.set_dfar(BitArray(length=32))  # unknown
                else:
                    self.core_registers.set_dfar(vaddress)
                if ldfsr_format:
                    dfsr_string[0] = self.tlb_lookup_came_from_cache_maintenance()
                    if dtype in (self.DAbort.DAbort_AsyncExternal, self.DAbort.DAbort_SyncExternal):
                        dfsr_string[1] = implementation_defined.dfsr_string_12
                    else:
                        dfsr_string[1] = False
                    if dtype in (self.DAbort.DAbort_SyncWatchpoint, self.DAbort.DAbort_AsyncWatchpoint):
                        dfsr_string[2] = False  # unknown
                    else:
                        dfsr_string[2] = iswrite
                    dfsr_string[3] = False  # unknown
                    dfsr_string[4] = True
                    dfsr_string[5:8] = "0b000"  # unknown
                    dfsr_string[8:] = self.encode_ldfsr(dtype, level)
                else:
                    if HaveLPAE():
                        dfsr_string[0] = self.tlb_lookup_came_from_cache_maintenance()
                    if dtype in (self.DAbort.DAbort_AsyncExternal, self.DAbort.DAbort_SyncExternal):
                        dfsr_string[1] = implementation_defined.dfsr_string_12
                    else:
                        dfsr_string[1] = False
                    if dtype in (self.DAbort.DAbort_SyncWatchpoint, self.DAbort.DAbort_AsyncWatchpoint):
                        dfsr_string[2] = False  # unknown
                    else:
                        dfsr_string[2] = iswrite
                    dfsr_string[4] = False
                    dfsr_string[5] = False  # unknown
                    domain_valid = (
                        dtype == self.DAbort.DAbort_Domain or
                        (
                            level == 2 and
                            dtype in (
                                self.DAbort.DAbort_Translation,
                                self.DAbort.DAbort_AccessFlag,
                                self.DAbort.DAbort_SyncExternalonWalk,
                                self.DAbort.DAbort_SyncParityonWalk
                            )
                        ) or (not HaveLPAE() and dtype == self.DAbort.DAbort_Permission))
                    if domain_valid:
                        dfsr_string[6:10] = domain
                    else:
                        dfsr_string[6:10] = "0b0000"  # unknown
                    temp_sdfsr = self.encode_sdfsr(dtype, level)
                    dfsr_string[3] = temp_sdfsr[0]
                    dfsr_string[10:14] = temp_sdfsr[1:5]
                self.core_registers.set_dfsr(dfsr_string)
            else:
                hsr_string = BitArray(length=25)
                ec = BitArray(length=6)
                self.core_registers.set_hdfar(vaddress)
                if ipavalid:
                    self.core_registers.set_hpfar(ipaddress[0:28])
                if secondstageabort:
                    ec[0:6] = "0b100100"
                    hsr_string[0:9] = self.ls_instruction_syndrome()
                else:
                    ec[0:6] = "0b100101"
                    hsr_string[0] = False
                if dtype in (self.DAbort.DAbort_AsyncExternal, self.DAbort.DAbort_SyncExternal):
                    hsr_string[15] = implementation_defined.data_abort_hsr_9
                hsr_string[16] = self.tlb_lookup_came_from_cache_maintenance()
                hsr_string[17] = s2fs1walk
                hsr_string[18] = iswrite
                hsr_string[19:25] = self.encode_ldfsr(dtype, level)
                self.write_hsr(ec, hsr_string)
        else:
            dfsr_string = BitArray(length=14)
            if (dtype in (
                    self.DAbort.DAbort_AsyncParity,
                    self.DAbort.DAbort_AsyncExternal,
                    self.DAbort.DAbort_AsyncWatchpoint
                ) or
                    (dtype == self.DAbort.DAbort_SyncWatchpoint and
                        int(self.core_registers.get_dbgdidr_version()) <= 4)):
                self.core_registers.set_dfar(BitArray(length=32))  # unknown
            elif dtype == self.DAbort.DAbort_SyncParity:
                if implementation_defined.data_abort_pmsa_change_dfar:
                    self.core_registers.set_dfar(vaddress)
            else:
                self.core_registers.set_dfar(vaddress)
            if dtype in (self.DAbort.DAbort_AsyncExternal, self.DAbort.DAbort_SyncExternal):
                dfsr_string[1] = implementation_defined.dfsr_string_12
            else:
                dfsr_string[1] = False
            if dtype in (self.DAbort.DAbort_SyncWatchpoint, self.DAbort.DAbort_AsyncWatchpoint):
                dfsr_string[2] = False  # unknown
            else:
                dfsr_string[2] = iswrite
            temp_pmsafsr = self.encode_pmsafsr(dtype, level)
            dfsr_string[3] = temp_pmsafsr[0]
            dfsr_string[10:14] = temp_pmsafsr[1:5]
            self.core_registers.set_dfsr(dfsr_string)
        raise DataAbortException()

    def alignment_fault_v(self, address, iswrite, taketohyp, secondstageabort):
        ipaddress = BitArray(length=40)  # unknown
        domain = BitArray(length=4)  # unknown
        level = 0  # unknown
        ipavalid = False
        ldfsr_fromat = taketohyp or self.core_registers.ttbcr.get_eae()
        s2fs1walk = False
        mva = self.fcse_translate(address)
        self.data_abort(mva, ipaddress, domain, level, iswrite, self.DAbort.DAbort_Alignment, taketohyp,
                        secondstageabort, ipavalid, ldfsr_fromat, s2fs1walk)

    def alignment_fault_p(self, address, iswrite):
        ipaddress = BitArray(length=40)  # unknown
        domain = BitArray(length=4)  # unknown
        level = 0  # unknown
        taketohypmode = False
        secondstageabort = False
        ipavalid = False
        ldfsr_fromat = False
        s2fs1walk = False
        self.data_abort(address, ipaddress, domain, level, iswrite, self.DAbort.DAbort_Alignment, taketohypmode,
                        secondstageabort, ipavalid, ldfsr_fromat, s2fs1walk)

    def alignment_fault(self, address, iswrite):
        if MemorySystemArchitecture() == MemArch.MemArch_VMSA:
            taketohypmode = self.core_registers.current_mode_is_hyp() or self.core_registers.hcr.get_tge()
            secondstageabort = False
            self.alignment_fault_v(address, iswrite, taketohypmode, secondstageabort)
        elif MemorySystemArchitecture() == MemArch.MemArch_PMSA:
            self.alignment_fault_p(address, iswrite)

    def combine_s1s2_desc(self, s1desc, s2desc):
        result = AddressDescriptor()
        result.paddress = s2desc.paddress
        result.memattrs.innerattrs = BitArray(length=2)  # unknown
        result.memattrs.outerattrs = BitArray(length=2)  # unknown
        result.memattrs.innerhints = BitArray(length=2)  # unknown
        result.memattrs.outerhints = BitArray(length=2)  # unknown
        result.memattrs.shareable = True
        result.memattrs.outershareable = True
        if (s2desc.memattrs.type == MemType.MemType_StronglyOrdered or
                s1desc.memattrs.type == MemType.MemType_StronglyOrdered):
            result.memattrs.type = MemType.MemType_StronglyOrdered
        elif s2desc.memattrs.type == MemType.MemType_Device or s1desc.memattrs.type == MemType.MemType_Device:
            result.memattrs.type = MemType.MemType_Device
        else:
            result.memattrs.type = MemType.MemType_Normal
        if result.memattrs.type == MemType.MemType_Normal:
            if s2desc.memattrs.innerattrs == "0b01" or s1desc.memattrs.innerattrs == "0b01":
                result.memattrs.innerattrs = BitArray(length=2)  # unknown
            elif s2desc.memattrs.innerattrs == "0b00" or s1desc.memattrs.innerattrs == "0b00":
                result.memattrs.innerattrs[0:2] = "0b00"
            elif s2desc.memattrs.innerattrs == "0b10" or s1desc.memattrs.innerattrs == "0b10":
                result.memattrs.innerattrs[0:2] = "0b10"
            else:
                result.memattrs.innerattrs[0:2] = "0b11"
            if s2desc.memattrs.outerattrs == "0b01" or s1desc.memattrs.outerattrs == "0b01":
                result.memattrs.outerattrs = BitArray(length=2)  # unknown
            elif s2desc.memattrs.outerattrs == "0b00" or s1desc.memattrs.outerattrs == "0b00":
                result.memattrs.outerattrs[0:2] = "0b00"
            elif s2desc.memattrs.outerattrs == "0b10" or s1desc.memattrs.outerattrs == "0b10":
                result.memattrs.outerattrs[0:2] = "0b10"
            else:
                result.memattrs.outerattrs[0:2] = "0b11"
            result.memattrs.innerhints = s1desc.memattrs.innerhints
            result.memattrs.outerhints = s1desc.memattrs.outerhints
            result.memattrs.shareable = s1desc.memattrs.shareable or s2desc.memattrs.shareable
            result.memattrs.outershareable = s1desc.memattrs.outershareable or s2desc.memattrs.outershareable
            # another check for normal memtype according to the documentation
            if result.memattrs.innerattrs == "0b00" and result.memattrs.outerattrs == "0b00":
                result.memattrs.shareable = True
                result.memattrs.outershareable = True
        return result

    def mair_decode(self, attr):
        memattrs = MemoryAttributes()
        if self.core_registers.current_mode_is_hyp():
            mair = self.core_registers.HMAIR1 + self.core_registers.HMAIR0
        else:
            mair = self.core_registers.MAIR1 + self.core_registers.MAIR0
        index = attr.uint
        attrfield = mair[56 - (8 * index):64 - (8 * index)]
        if attrfield[0:4] == "0b0000":
            unpackinner = False
            memattrs.innerattrs = BitArray(length=2)  # unknown
            memattrs.outerattrs = BitArray(length=2)  # unknown
            memattrs.innerhints = BitArray(length=2)  # unknown
            memattrs.outerhints = BitArray(length=2)  # unknown
            memattrs.innertransient = False  # unknown
            memattrs.outertransient = False  # unknown
            if attrfield[4:8] == "0b0000":
                memattrs.type = MemType.MemType_StronglyOrdered
            elif attrfield[4:8] == "0b0100":
                memattrs.type = MemType.MemType_Device
            else:
                # implementation defined:
                memattrs.type = MemType.MemType_Device
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.innertransient = False  # unknown
                memattrs.outertransient = False  # unknown
        elif attrfield[0:2] == "0b00":
            unpackinner = True
            if ImplementationSupportsTransient():
                memattrs.type = MemType.MemType_Normal
                memattrs.outerhints = attrfield[2:4]
                memattrs.outerattrs[0:2] = "0b10"
                memattrs.outertransient = True
            else:
                # implementation defined:
                memattrs.type = MemType.MemType_Normal
                memattrs.outerhints[0:2] = "0b00"
                memattrs.outerattrs[0:2] = "0b00"
                memattrs.outertransient = False
        elif attrfield[0:2] == "0b01":
            unpackinner = True
            if attrfield[2:4] == "0b00":
                memattrs.type == MemType.MemType_Normal
                memattrs.outerhints[0:2] = "0b00"
                memattrs.outerattrs[0:2] = "0b00"
                memattrs.outertransient = False
            else:
                if ImplementationSupportsTransient():
                    memattrs.type = MemType.MemType_Normal
                    memattrs.outerhints = attrfield[2:4]
                    memattrs.outerattrs[0:2] = "0b11"
                    memattrs.outertransient = True
                else:
                    # implementation defined:
                    memattrs.type == MemType.MemType_Normal
                    memattrs.outerhints[0:2] = "0b00"
                    memattrs.outerattrs[0:2] = "0b00"
                    memattrs.outertransient = False
        else:
            unpackinner = True
            memattrs.type = MemType.MemType_Normal
            memattrs.outerhints = attrfield[2:4]
            memattrs.outerattrs = attrfield[0:2]
            memattrs.outertransient = False
        if unpackinner:
            if attrfield[4]:
                memattrs.innerhints = attrfield[6:8]
                memattrs.innerattrs = attrfield[4:6]
                memattrs.innertransient = False
            elif attrfield[5:8]:
                memattrs.innerhints[0:2] = "0b00"
                memattrs.innerattrs[0:2] = "0b00"
                memattrs.innertransient = True
            else:
                if ImplementationSupportsTransient():
                    if not attrfield[5]:
                        memattrs.innerhints = attrfield[6:8]
                        memattrs.innerattrs[0:2] = "0b10"
                        memattrs.innertransient = True
                    else:
                        memattrs.innerhints = attrfield[6:8]
                        memattrs.innerattrs[0:2] = "0b11"
                        memattrs.innertransient = True
                else:
                    # implementation defined:
                    memattrs.type = MemType.MemType_Normal
                    memattrs.innerattrs = BitArray(length=2)  # unknown
                    memattrs.outerattrs = BitArray(length=2)  # unknown
                    memattrs.innerhints = BitArray(length=2)  # unknown
                    memattrs.outerhints = BitArray(length=2)  # unknown
                    memattrs.innertransient = False  # unknown
                    memattrs.outertransient = False  # unknown
        return memattrs

    def s2_attr_decode(self, attr):
        memattrs = MemoryAttributes()
        if attr[0:2] == "0b00":
            memattrs.innerattrs = BitArray(length=2)  # unknown
            memattrs.outerattrs = BitArray(length=2)  # unknown
            memattrs.innerhints = BitArray(length=2)  # unknown
            memattrs.outerhints = BitArray(length=2)  # unknown
            if attr[2:4] == "0b00":
                memattrs.type = MemType.MemType_StronglyOrdered
            elif attr[2:4] == "0b01":
                memattrs.type = MemType.MemType_Device
            else:
                memattrs.type = MemType.MemType_Normal  # unknown
        else:
            memattrs.type = MemType.MemType_Normal
            if not attr[0]:
                memattrs.outerattrs[0:2] = "0b00"
                memattrs.outerhints[0:2] = "0b00"
            else:
                memattrs.outerattrs[0:2] = attr[0:2]
                memattrs.outerhints[0:2] = "0b11"
            if attr[2:4] == "0b00":
                memattrs.type = MemType.MemType_Normal  # unknown
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
            elif not attr[2]:
                memattrs.innerattrs[0:2] = "0b00"
                memattrs.innerhints[0:2] = "0b00"
            else:
                memattrs.innerattrs[0:2] = "0b11"
                memattrs.innerhints[0:2] = attr[2:4]
        return memattrs

    def remap_regs_have_reset_values(self):
        # mock
        raise NotImplementedError()

    def default_tex_decode(self, texcb, s):
        memattrs = MemoryAttributes()
        if texcb == "0b00000":
            memattrs.type = MemType.MemType_StronglyOrdered
            memattrs.innerattrs = BitArray(length=2)  # unknown
            memattrs.innerhints = BitArray(length=2)  # unknown
            memattrs.outerattrs = BitArray(length=2)  # unknown
            memattrs.outerhints = BitArray(length=2)  # unknown
            memattrs.shareable = True
        elif texcb == "0b00001":
            memattrs.type = MemType.MemType_Device
            memattrs.innerattrs = BitArray(length=2)  # unknown
            memattrs.innerhints = BitArray(length=2)  # unknown
            memattrs.outerattrs = BitArray(length=2)  # unknown
            memattrs.outerhints = BitArray(length=2)  # unknown
            memattrs.shareable = True
        elif texcb == "0b00010":
            memattrs.type = MemType.MemType_Normal
            memattrs.innerattrs[0:2] = "0b10"
            memattrs.innerhints[0:2] = "0b10"
            memattrs.outerattrs[0:2] = "0b10"
            memattrs.outerhints[0:2] = "0b10"
            memattrs.shareable = s
        elif texcb == "0b00011":
            memattrs.type = MemType.MemType_Normal
            memattrs.innerattrs[0:2] = "0b11"
            memattrs.innerhints[0:2] = "0b10"
            memattrs.outerattrs[0:2] = "0b11"
            memattrs.outerhints[0:2] = "0b10"
            memattrs.shareable = s
        elif texcb == "0b00100":
            memattrs.type = MemType.MemType_Normal
            memattrs.innerattrs[0:2] = "0b00"
            memattrs.innerhints[0:2] = "0b00"
            memattrs.outerattrs[0:2] = "0b00"
            memattrs.outerhints[0:2] = "0b00"
            memattrs.shareable = s
        elif texcb == "0b00110":
            # implemetation defined
            pass
        elif texcb == "0b00111":
            memattrs.type = MemType.MemType_Normal
            memattrs.innerattrs[0:2] = "0b11"
            memattrs.innerhints[0:2] = "0b11"
            memattrs.outerattrs[0:2] = "0b11"
            memattrs.outerhints[0:2] = "0b11"
            memattrs.shareable = s
        elif texcb == "0b01000":
            memattrs.type = MemType.MemType_Device
            memattrs.innerattrs[0:2] = "0b10"
            memattrs.innerhints[0:2] = "0b10"
            memattrs.outerattrs[0:2] = "0b10"
            memattrs.outerhints[0:2] = "0b10"
            memattrs.shareable = True  # has to be false
        elif texcb[0]:
            memattrs.type = MemType.MemType_Normal
            hintsattrs = self.convert_attrs_hints(texcb[3:5])
            memattrs.innerattrs = hintsattrs[2:4]
            memattrs.innerhints = hintsattrs[0:2]
            hintsattrs = self.convert_attrs_hints(texcb[1:3])
            memattrs.outerattrs = hintsattrs[2:4]
            memattrs.outerhints = hintsattrs[0:2]
            memattrs.shareable = s
        else:
            print "unpredictable"
        memattrs.outershareable = memattrs.shareable
        return memattrs

    def remapped_tex_decode(self, texcb, s):
        memattrs = MemoryAttributes()
        hintsattrs = BitArray(length=4)
        region = texcb[2:5].uint
        if region == 6:
            raise NotImplementedError()
            # IMPLEMENTATION_DEFINED setting of memattrs
            pass
        else:
            if self.core_registers.prrr.get_tr_n(region) == "0b00":
                memattrs.type = MemType.MemType_StronglyOrdered
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.core_registers.prrr.get_tr_n(region) == "0b01":
                memattrs.type = MemType.MemType_Device
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.core_registers.prrr.get_tr_n(region) == "0b10":
                memattrs.type = MemType.MemType_Normal
                hintsattrs = self.convert_attrs_hints(self.core_registers.nmrr.get_ir_n(region))
                memattrs.innerattrs = hintsattrs[2:4]
                memattrs.innerhints = hintsattrs[0:2]
                hintsattrs = self.convert_attrs_hints(self.core_registers.nmrr.get_or_n(region))
                memattrs.outerattrs = hintsattrs[2:4]
                memattrs.outerhints = hintsattrs[0:2]
                s_bit = self.core_registers.prrr.get_ns0() if not s else self.core_registers.prrr.get_ns1()
                memattrs.shareable = s_bit
                memattrs.outershareable = s_bit and not self.core_registers.prrr.get_nos_n(region)
            elif self.core_registers.prrr.get_tr_n(region) == "0b11":
                memattrs.type = MemType.MemType_Normal  # unknown
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.shareable = False  # unknown
                memattrs.outershareable = False  # unknown
        return memattrs

    def translation_table_walk_ld(self, ia, va, is_write, stage1, s2fs1walk, size):
        result = TLBRecord()
        walkaddr = AddressDescriptor()
        domain = BitArray(length=4)  # unknown
        ldfsr_format = True
        base_address = BitArray(length=40)
        base_found = False
        disabled = False
        if stage1:
            if self.core_registers.current_mode_is_hyp():
                lookup_secure = False
                t0_size = self.core_registers.htcr.get_t0sz().uint
                if t0_size == 0 or ia[8:t0_size + 8].uint == 0:
                    current_level = 1 if self.core_registers.htcr.get_t0sz()[0:2] == "0b00" else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = self.core_registers.HTTBR[24:64 - ba_lower_bound] + BitArray(length=ba_lower_bound)
                    if self.core_registers.HTTBR[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.core_registers.htcr.get_irgn0())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.core_registers.htcr.get_orgn0())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.core_registers.htcr.get_sh0()[0]
                    walkaddr.memattrs.outershareable = self.core_registers.htcr.get_sh0() == "0b10"
                    walkaddr.paddress.ns = True
            else:
                lookup_secure = self.core_registers.is_secure()
                t0_size = self.core_registers.ttbcr.get_t0sz().uint
                if t0_size == 0 or ia[8:t0_size + 8].uint == 0:
                    current_level = 1 if self.core_registers.ttbcr.get_t0sz().bin[0:2] == "00" else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = self.core_registers.TTBR0_64[24:64 - ba_lower_bound] + BitArray(
                        length=ba_lower_bound)
                    if self.core_registers.TTBR0_64[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    disabled = self.core_registers.ttbcr.get_epd0()
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.core_registers.ttbcr.get_irgn0())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.core_registers.ttbcr.get_orgn0())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.core_registers.ttbcr.get_sh0()[0]
                    walkaddr.memattrs.outershareable = self.core_registers.ttbcr.get_sh0() == "0b10"
                t1_size = self.core_registers.ttbcr.get_t1sz().uint
                if (t1_size == 0 and not base_found) or ia[8:t1_size + 8].all(True):
                    current_level = 1 if self.core_registers.ttbcr.get_t1sz().bin[0:2] == "00" else 2
                    ba_lower_bound = 9 * current_level - t1_size - 4
                    base_address = self.core_registers.TTBR1_64[24:64 - ba_lower_bound] + BitArray(
                        length=ba_lower_bound)
                    if self.core_registers.TTBR1_64[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    disabled = self.core_registers.ttbcr.get_epd1()
                    start_bit = 31 - t1_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.core_registers.ttbcr.get_irgn1())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.core_registers.ttbcr.get_orgn1())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.core_registers.ttbcr.get_sh1()[0]
                    walkaddr.memattrs.outershareable = self.core_registers.ttbcr.get_sh1() == "0b10"
        else:
            t0_size = self.core_registers.vtcr.get_t0sz().uint
            s_level = self.core_registers.vtcr.get_sl0().uint
            ba_lower_bound = 14 - t0_size - (9 * s_level)
            if s_level == 0 and t0_size < -2:
                print "unpredictable"
            if s_level == 1 and t0_size > 1:
                print "unpredictable"
            if self.core_registers.vtcr.get_sl0()[0]:
                print "unpredictable"
            if self.core_registers.VTTBR[64 - ba_lower_bound:61].uint != 0:
                print "unpredictable"
            if t0_size == -8 or ia[0:t0_size + 8].uint == 0:
                current_level = 2 - s_level
                base_address = self.core_registers.VTTBR[24:64 - ba_lower_bound] + BitArray(length=ba_lower_bound)
                base_found = True
                start_bit = 31 - t0_size
            lookup_secure = False
            walkaddr.memattrs.type = MemType.MemType_Normal
            hintsattrs = self.convert_attrs_hints(self.core_registers.vtcr.get_irgn0())
            walkaddr.memattrs.innerhints = hintsattrs[0:2]
            walkaddr.memattrs.innerattrs = hintsattrs[2:4]
            hintsattrs = self.convert_attrs_hints(self.core_registers.vtcr.get_orgn0())
            walkaddr.memattrs.outerhints = hintsattrs[0:2]
            walkaddr.memattrs.outerattrs = hintsattrs[2:4]
            walkaddr.memattrs.shareable = self.core_registers.vtcr.get_sh0()[0]
            walkaddr.memattrs.outershareable = self.core_registers.vtcr.get_sh0() == "0b10"
        if not base_found or disabled:
            taketohypmode = self.core_registers.current_mode_is_hyp() or not stage1
            level = 1
            ipavalid = not stage1
            self.data_abort(va, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, not stage1,
                            ipavalid, ldfsr_format, s2fs1walk)
        first_iteration = True
        table_rw = True
        table_user = True
        table_xn = False
        table_pxn = False
        lookup_finished = True
        output_address = BitArray(length=40)
        attrs = BitArray(length=13)
        while lookup_finished:
            lookup_finished = True
            block_translate = False
            offset = 9 * current_level
            if first_iteration:
                ia_select = bits_ops.zero_extend(ia[39 - start_bit:offset + 1] + "0b000", 40)
            else:
                ia_select = bits_ops.zero_extend(ia[offset - 8:offset + 1] + "0b000", 40)
            lookup_address = base_address | ia_select
            first_iteration = False
            walkaddr.paddress.physicaladdress = lookup_address
            if lookup_secure:
                walkaddr.paddress.ns = False
            else:
                walkaddr.paddress.ns = True
            if (not HaveVirtExt() or
                    not stage1 or
                    self.core_registers.is_secure() or
                    self.core_registers.current_mode_is_hyp()):
                if HaveVirtExt() and (self.core_registers.current_mode_is_hyp() or not stage1):
                    big_endian = self.core_registers.hsctlr.get_ee()
                else:
                    big_endian = self.core_registers.sctlr.get_ee()
                descriptor = self.mem[walkaddr, 8]
                if big_endian:
                    descriptor = self.big_endian_reverse(descriptor, 8)
            else:
                walkaddr2 = self.second_stage_translate(walkaddr, ia[8:40], 8, is_write)
                descriptor = self.mem[walkaddr2, 8]
                if self.core_registers.sctlr.get_ee():
                    descriptor = self.big_endian_reverse(descriptor, 8)
            if not descriptor[-1]:
                taketohypmode = self.core_registers.current_mode_is_hyp() or not stage1
                ipavalid = not stage1
                self.data_abort(va, ia, domain, current_level, is_write, self.DAbort.DAbort_Translation, taketohypmode,
                                not stage1, ipavalid, ldfsr_format, s2fs1walk)
            else:
                if not descriptor[-2]:
                    if current_level == 3:
                        taketohypmode = self.core_registers.current_mode_is_hyp() or not stage1
                        ipavalid = not stage1
                        self.data_abort(va, ia, domain, current_level, is_write, self.DAbort.DAbort_Translation,
                                        taketohypmode, not stage1, ipavalid, ldfsr_format, s2fs1walk)
                    else:
                        block_translate = True
                else:
                    if current_level == 3:
                        block_translate = True
                    else:
                        base_address = descriptor[24:52] + "0b000000000000"
                        lookup_secure = lookup_secure and not descriptor[0]
                        table_rw = table_rw and not descriptor[1]
                        table_user = table_user and not descriptor[2]
                        table_pxn = table_pxn or descriptor[4]
                        table_xn = table_xn or descriptor[3]
                        lookup_finished = False
            if block_translate:
                output_address = descriptor[24:25 + offset] + ia[offset + 1:40]
                attrs = descriptor[9:12] + descriptor[52:62]
                if stage1:
                    if table_xn:
                        attrs[0] = True
                    if table_pxn:
                        attrs[1] = True
                    if self.core_registers.is_secure() and not lookup_secure:
                        attrs[3] = True
                    if not table_rw:
                        attrs[7] = True
                    if not table_user:
                        attrs[8] = False
                    if not lookup_secure:
                        attrs[9] = True
            else:
                current_level += 1
        if not attrs[4]:
            taketohypmode = self.core_registers.current_mode_is_hyp() or not stage1
            ipavalid = not stage1
            self.data_abort(va, ia, domain, current_level, is_write, self.DAbort.DAbort_AccessFlag, taketohypmode,
                            not stage1, ipavalid, ldfsr_format, s2fs1walk)
        result.perms.xn = attrs[0]
        result.perms.pxn = attrs[1]
        result.contiguousbit = attrs[2]
        result.ng = attrs[3]
        result.perms.ap[0:2] = attrs[7:9]
        result.perms.ap[2] = True
        if stage1:
            result.addrdesc.memattrs = self.mair_decode(attrs[10:13])
        else:
            result.addrdesc.memattrs = self.s2_attr_decode(attrs[9:13])
        if result.addrdesc.memattrs.type == MemType.MemType_Normal:
            result.addrdesc.memattrs.shareable = attrs[5]
            result.addrdesc.memattrs.outershareable = attrs[5:7] == "0b10"
        else:
            result.addrdesc.memattrs.shareable = True
            result.addrdesc.memattrs.outershareable = True
        result.domain = BitArray(length=4)  # unknown
        result.level = current_level
        result.blocksize = (512 ** (3 - current_level)) * 4
        result.addrdesc.paddress.physicaladdress = output_address[-40:]
        if stage1:
            result.addrdesc.paddress.ns = attrs[9]
        else:
            result.addrdesc.paddress.ns = True
        if stage1 and self.core_registers.current_mode_is_hyp():
            if not attrs[8]:
                print "unpredictable"
            if not table_user:
                print "unpredictable"
            if attrs[1]:
                print "unpredictable"
            if not table_pxn:
                print "unpredictable"
            if attrs[3]:
                print "unpredictable"
        return result

    def translation_table_walk_sd(self, mva, is_write, size):
        result = TLBRecord()
        l1descaddr = AddressDescriptor()
        l2descaddr = AddressDescriptor()
        taketohypmode = False
        ia = BitArray(length=40)  # unknown
        ipavalid = False
        stage2 = False
        ldfsr_format = False
        s2fs1walk = False
        domain = BitArray(length=4)  # unknown
        ttbr = BitArray(length=64)
        n = self.core_registers.ttbcr.get_n().uint
        if n == 0 or mva[0:n + 1].uint == 0:
            ttbr = self.core_registers.TTBR0_64
            disabled = self.core_registers.ttbcr.get_pd1()
        else:
            ttbr = self.core_registers.TTBR1_64
            disabled = self.core_registers.ttbcr.get_pd1()
            n = 0
        if HaveSecurityExt() and disabled:
            level = 1
            self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, stage2,
                            ipavalid, ldfsr_format, s2fs1walk)
        l1descaddr.paddress.physicaladdress = "0b00000000" + ttbr[32:n + 50] + mva[n:12] + "0b00"
        l1descaddr.paddress.ns = not self.core_registers.is_secure()
        l1descaddr.memattrs.type = MemType.MemType_Normal
        l1descaddr.memattrs.shareable = ttbr[62]
        l1descaddr.memattrs.outershareable = ttbr[62] and not ttbr[58]
        hintsattrs = self.convert_attrs_hints(ttbr[59:61])
        l1descaddr.memattrs.outerattrs = hintsattrs[2:4]
        l1descaddr.memattrs.outerhints = hintsattrs[0:2]
        if HaveMPExt():
            hintsattrs = self.convert_attrs_hints(ttbr[63:64] + ttbr[57:58])
            l1descaddr.memattrs.innerattrs = hintsattrs[2:4]
            l1descaddr.memattrs.innerhints = hintsattrs[0:2]
        else:
            if not ttbr[63]:
                hintsattrs = self.convert_attrs_hints(BitArray(bin="00"))
                l1descaddr.memattrs.innerattrs = hintsattrs[2:4]
                l1descaddr.memattrs.innerhints = hintsattrs[0:2]
            else:
                l1descaddr.memattrs.innerattrs[0:2] = ("0b10"
                                                       if implementation_defined.translation_walk_sd_l1descaddr_attrs_10
                                                       else "0b11")
                l1descaddr.memattrs.innerhints[0:2] = ("0b01"
                                                       if implementation_defined.translation_walk_sd_l1descaddr_hints_01
                                                       else "0b11")
        if not HaveVirtExt() or self.core_registers.is_secure():
            l1descaddr2 = l1descaddr
        else:
            l1descaddr2 = self.second_stage_translate(l1descaddr, mva, 4, is_write)
        l1desc = self.mem[l1descaddr2, 4]
        if self.core_registers.sctlr.get_ee():
            l1desc = self.big_endian_reverse(l1desc, 4)
        if l1desc[30:32] == "0b00":
            level = 1
            self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, stage2,
                            ipavalid, ldfsr_format, s2fs1walk)
        elif l1desc[30:32] == "0b01":
            domain = l1desc[23:27]
            level = 2
            pxn = l1desc[29]
            ns = l1desc[28]
            l2descaddr.paddress.physicaladdress = "0b00000000" + l1desc[0:22] + mva[12:20] + "0b00"
            l2descaddr.paddress.ns = not self.core_registers.is_secure()
            l2descaddr.memattrs = l1descaddr.memattrs
            if not HaveVirtExt() or self.core_registers.is_secure():
                l2descaddr2 = l2descaddr
            else:
                l2descaddr2 = self.second_stage_translate(l2descaddr, mva, 4, is_write)
            l2desc = self.mem[l2descaddr2, 4]
            if self.core_registers.sctlr.get_ee():
                l2desc = self.big_endian_reverse(l2desc, 4)
            if l2desc[30:32] == "0b00":
                self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, stage2,
                                ipavalid, ldfsr_format, s2fs1walk)
            s = l2desc[21]
            ap = l2desc[22:23] + l2desc[26:28]
            ng = l2desc[20]
            if self.core_registers.sctlr.get_afe() and not l2desc[27]:
                if not self.core_registers.sctlr.get_ha():
                    self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_AccessFlag, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.core_registers.sctlr.get_ee():
                        self.mem.set_bits(l2descaddr2, 4, 3, 1, BitArray(bin="1"))
                    else:
                        self.mem.set_bits(l2descaddr2, 4, 27, 1, BitArray(bin="1"))
            if not l2desc[30]:
                texcb = l2desc[17:20] + l2desc[28:30]
                xn = l2desc[16]
                block_size = 64
                physicaladdressext = BitArray(bin="00000000")
                physicaladdress = l2desc[0:16] + mva[16:32]
            else:
                texcb = l2desc[23:26] + l2desc[28:30]
                xn = l2desc[31]
                block_size = 4
                physicaladdressext = BitArray(bin="00000000")
                physicaladdress = l2desc[0:20] + mva[20:32]
        elif l1desc[30]:
            texcb = l1desc[17:20] + l1desc[28:30]
            s = l1desc[15]
            ap = l1desc[16:17] + l1desc[20:22]
            xn = l1desc[27]
            pxn = l1desc[31]
            ng = l1desc[14]
            level = 1
            ns = l1desc[12]
            if self.core_registers.sctlr.get_afe() and not l1desc[21]:
                if not self.core_registers.sctlr.get_ha():
                    self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_AccessFlag, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.core_registers.sctlr.get_ee():
                        self.mem.set_bits(l1descaddr2, 4, 13, 1, BitArray(bin="1"))
                    else:
                        self.mem.set_bits(l1descaddr2, 4, 21, 1, BitArray(bin="1"))
            if not l1desc[13]:
                domain = l1desc[23:27]
                block_size = 1024
                physicaladdressext = BitArray(bin="00000000")
                physicaladdress = l1desc[0:12] + mva[12:32]
            else:
                domain = BitArray(bin="0000")
                block_size = 16384
                physicaladdressext = l1desc[23:27] + l1desc[8:12]
                physicaladdress = l1desc[0:8] + mva[8:32]
        if not self.core_registers.sctlr.get_tre():
            if self.remap_regs_have_reset_values():
                result.addrdesc.memattrs = self.default_tex_decode(texcb, s)
            else:
                # IMPLEMENTATION_DEFINED setting of result.addrdesc.memattrs
                pass
        else:
            result.addrdesc.memattrs = self.remapped_tex_decode(texcb, s)
        result.addrdesc.memattrs.innertransient = False
        result.addrdesc.memattrs.outertransient = False
        result.perms.ap = ap
        result.perms.xn = xn
        result.perms.pxn = pxn
        result.ng = ng
        result.domain = domain
        result.level = level
        result.blocksize = block_size
        result.addrdesc.paddress.physicaladdress = physicaladdressext + physicaladdress
        result.addrdesc.paddress.ns = ns if self.core_registers.is_secure() else True
        return result

    def translate_address_v_s1_off(self, va):
        result = TLBRecord()
        if (not HaveVirtExt() or
                not self.core_registers.hcr.get_dc() or
                self.core_registers.is_secure() or
                self.core_registers.current_mode_is_hyp()):
            result.addrdesc.memattrs.type = MemType.MemType_StronglyOrdered
            result.addrdesc.memattrs.innerattrs = BitArray(length=2)  # unknown
            result.addrdesc.memattrs.innerhints = BitArray(length=2)  # unknown
            result.addrdesc.memattrs.outerattrs = BitArray(length=2)  # unknown
            result.addrdesc.memattrs.outerhints = BitArray(length=2)  # unknown
            result.addrdesc.memattrs.shareable = True
            result.addrdesc.memattrs.outershareable = True
        else:
            result.addrdesc.memattrs.type = MemType.MemType_Normal
            result.addrdesc.memattrs.innerattrs[0:2] = "0b11"
            result.addrdesc.memattrs.innerhints[0:2] = "0b11"
            result.addrdesc.memattrs.outerattrs[0:2] = "0b11"
            result.addrdesc.memattrs.outerhints[0:2] = "0b11"
            result.addrdesc.memattrs.shareable = False
            result.addrdesc.memattrs.outershareable = False
            if not self.core_registers.hcr.get_vm():
                print "unpredictable"
        result.perms.ap = BitArray(length=3)  # unknown
        result.perms.xn = False
        result.perms.pxn = False
        result.ng = False  # unknown
        result.domain = BitArray(length=4)  # unknown
        result.level = 0  # unknown
        result.blocksize = 0  # unknown
        result.addrdesc.paddress.physicaladdress = "0b00000000" + va
        result.addrdesc.paddress.ns = not self.core_registers.is_secure()
        return result

    def translate_address_v(self, va, ispriv, iswrite, size, wasaligned):
        result = AddressDescriptor()
        s2fs1walk = False
        mva = self.fcse_translate(va)
        ishyp = self.core_registers.current_mode_is_hyp()
        if (ishyp and self.core_registers.hsctlr.get_m()) or (not ishyp and self.core_registers.sctlr.get_m()):
            if (HaveVirtExt() and
                    not self.core_registers.is_secure() and
                    not ishyp and
                    self.core_registers.hcr.get_tge()):
                print "unpredictable"
            uses_ld = ishyp or self.core_registers.ttbcr.get_eae()
            if uses_ld:
                ia_in = BitArray(bin="00000000") + mva
                tlbrecordS1 = self.translation_table_walk_ld(ia_in, mva, iswrite, True, s2fs1walk, size)
                check_domain = False
                check_permission = True
            else:
                tlbrecordS1 = self.translation_table_walk_sd(mva, iswrite, size)
                check_domain = True
                check_permission = True
        else:
            tlbrecordS1 = self.translate_address_v_s1_off(mva)
            check_domain = False
            check_permission = False
        if (not wasaligned and
                tlbrecordS1.addrdesc.memattrs.type in (MemType.MemType_StronglyOrdered, MemType.MemType_Device)):
            if not HaveVirtExt():
                print "unpredictable"
            secondstageabort = False
            self.alignment_fault_v(mva, iswrite, ishyp, secondstageabort)
        if check_domain:
            check_permission = self.check_domain(tlbrecordS1.domain, mva, tlbrecordS1.level, iswrite)
        if check_permission:
            self.check_permission(tlbrecordS1.perms, mva, tlbrecordS1.level, tlbrecordS1.domain, iswrite, ispriv, ishyp,
                                  uses_ld)
        if HaveVirtExt() and not self.core_registers.is_secure() and not ishyp:
            if self.core_registers.hcr.get_vm():
                s1outputaddr = tlbrecordS1.addrdesc.paddress.physicaladdress
                tlbrecordS2 = self.translation_table_walk_ld(s1outputaddr, mva, iswrite, False, s2fs1walk, size)
                if (not wasaligned and
                        tlbrecordS2.addrdesc.memattrs.type in (
                                MemType.MemType_Device,
                                MemType.MemType_StronglyOrdered
                        )):
                    taketohypmode = True
                    secondstageabort = True
                    self.alignment_fault_v(mva, iswrite, taketohypmode, secondstageabort)
                self.check_permission_s2(tlbrecordS2.perms, mva, s1outputaddr, tlbrecordS2.level, iswrite, s2fs1walk)
                result = self.combine_s1s2_desc(tlbrecordS1.addrdesc, tlbrecordS2.addrdesc)
            else:
                result = tlbrecordS1.addrdesc
        else:
            result = tlbrecordS1.addrdesc
        return result

    def translate_address_p(self, va, ispriv, iswrite, wasaligned):
        result = AddressDescriptor()
        perms = Permissions
        result.paddress.physicaladdress = "0b00000000" + va
        # IMPLEMENTATION_DEFINED setting of result.paddress.NS;
        if not self.core_registers.sctlr.get_m():
            result.memattrs = self.default_memory_attributes(va)
        else:
            region_found = False
            texcb = BitArray(length=5)  # unknown
            s = False  # unknown
            for r in xrange(self.core_registers.mpuir.get_dregion().uint):
                size_enable = self.core_registers.drsrs[r]
                base_address = self.core_registers.DRBARs[r]
                access_control = self.core_registers.dracrs[r]
                if size_enable.get_en():
                    ls_bit = size_enable.get_rsize().uint + 1
                    if ls_bit < 2:
                        print "unpredictable"
                    if ls_bit > 2 and base_address[32 - ls_bit:30].uint != 0:
                        print "unpredictable"
                    if ls_bit == 32 or va[0:32 - ls_bit] == base_address[0:32 - ls_bit]:
                        if ls_bit >= 8:
                            subregion = va[32 - ls_bit:35 - ls_bit].uint
                            hit = not size_enable.get_sd_n(subregion)
                        else:
                            hit = True
                        if hit:
                            texcb = (access_control.get_tex() +
                                     BitArray(bool=access_control.get_c()) +
                                     BitArray(bool=access_control.get_b()))
                            s = access_control.get_s()
                            perms.ap = access_control.get_ap()
                            perms.xn = access_control.get_xn()
                            region_found = True
            if region_found:
                result.memattrs = self.default_tex_decode(texcb, s)
            else:
                if not self.core_registers.sctlr.get_br() or not ispriv:
                    ipaddress = BitArray(length=40)  # unknown
                    domain = BitArray(length=4)  # unkown
                    level = 0  # unkown
                    taketohypmode = False
                    secondstageabort = False
                    ipavalid = False
                    ldfsr_format = False
                    s2fs1walk = False
                    self.data_abort(va, ipaddress, domain, level, iswrite, self.DAbort.DAbort_Background, taketohypmode,
                                    secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    result.memattrs = self.default_memory_attributes(va)
                    perms.ap = BitArray(bin="011")
                    perms.xn = not self.core_registers.sctlr.get_v() if va[0:4] == "0b1111" else va[0]
                    perms.pxn = False
            if not wasaligned and result.memattrs.type in (MemType.MemType_Device, MemType.MemType_StronglyOrdered):
                print "unpredictable"
            self.check_permission(perms, va, 0, BitArray(length=4), iswrite, ispriv, False, False)
        return result

    def translate_address(self, va, ispriv, iswrite, size, wasaligned):
        if MemorySystemArchitecture() == MemArch.MemArch_VMSA:
            return self.translate_address_v(va, ispriv, iswrite, size, wasaligned)
        elif MemorySystemArchitecture() == MemArch.MemArch_PMSA:
            return self.translate_address_p(va, ispriv, iswrite, wasaligned)

    def is_exclusive_local(self, paddress, processor_id, size):
        # mock
        raise NotImplementedError()

    def is_exclusive_global(self, paddress, processor_id, size):
        # mock
        raise NotImplementedError()

    def clear_exclusive_local(self, processor_id):
        # mock
        raise NotImplementedError()
        pass

    def clear_exclusive_by_address(self, paddress, processor_id, size):
        # mock
        raise NotImplementedError()

    def mark_exclusive_global(self, paddress, processor_id, size):
        # mock
        raise NotImplementedError()
        pass

    def mark_exclusive_local(self, paddress, processor_id, size):
        # mock
        raise NotImplementedError()
        pass

    def exclusive_monitors_pass(self, address, size):
        if address != bits_ops.align(address, size):
            self.alignment_fault(address, True)
        else:
            memaddrdesc = self.translate_address(address, self.core_registers.current_mode_is_not_user(), True, size,
                                                 True)
        passed = self.is_exclusive_local(memaddrdesc.paddress, ProcessorID(), size)
        if passed:
            self.clear_exclusive_local(ProcessorID())
        if memaddrdesc.memattrs.shareable:
            passed = passed and self.is_exclusive_global(memaddrdesc.paddress, ProcessorID(), size)
        return passed

    def set_exclusive_monitors(self, address, size):
        memaddrdesc = self.translate_address(address, self.core_registers.current_mode_is_not_user(), False, size, True)
        if memaddrdesc.memattrs.shareable:
            self.mark_exclusive_global(memaddrdesc.paddress, ProcessorID(), size)
        self.mark_exclusive_local(memaddrdesc.paddress, ProcessorID(), size)

    def mem_a_with_priv_set(self, address, size, privileged, was_aligned, value):
        if address == bits_ops.align(address, size):
            va = address
        elif ArchVersion() >= 7 or self.core_registers.sctlr.get_a() or self.core_registers.sctlr.get_u():
            self.alignment_fault(address, True)
        else:
            va = bits_ops.align(address, size)
        memaddrdesc = self.translate_address(va, privileged, True, size, was_aligned)
        if memaddrdesc.memattrs.shareable:
            self.clear_exclusive_by_address(memaddrdesc.paddress, ProcessorID(), size)
        if self.core_registers.get_cpsr_e() == "1":
            value = self.big_endian_reverse(value, size)
        self.mem[memaddrdesc, size] = value

    def mem_a_with_priv_get(self, address, size, privileged, was_aligned):
        if address == bits_ops.align(address, size):
            va = address
        elif ArchVersion() >= 7 or self.core_registers.sctlr.get_a() or self.core_registers.sctlr.get_u():
            self.alignment_fault(address, False)
        else:
            va = bits_ops.align(address, size)
        memaddrdesc = self.translate_address(va, privileged, False, size, was_aligned)
        value = self.mem[memaddrdesc, size]
        if self.core_registers.get_cpsr_e() == "1":
            value = self.big_endian_reverse(value, size)
        return value

    def mem_a_set(self, address, size, value):
        self.mem_a_with_priv_set(address, size, self.core_registers.current_mode_is_not_user(), True, value)

    def mem_a_get(self, address, size):
        return self.mem_a_with_priv_get(address, size, self.core_registers.current_mode_is_not_user(), True)

    def mem_u_with_priv_set(self, address, size, privileged, value):
        if ArchVersion() < 7 and not self.core_registers.sctlr.get_a() and not self.core_registers.sctlr.get_u():
            address = bits_ops.align(address, size)
        if address == bits_ops.align(address, size):
            self.mem_a_with_priv_set(address, size, privileged, True, value)
        elif (HaveVirtExt() and
                not self.core_registers.is_secure() and
                self.core_registers.current_mode_is_hyp() and
                self.core_registers.hsctlr.get_a()):
            self.alignment_fault(address, True)
        elif not self.core_registers.current_mode_is_hyp() and self.core_registers.sctlr.get_a():
            self.alignment_fault(address, True)
        else:
            if self.core_registers.get_cpsr_e() == "1":
                value = self.big_endian_reverse(value, size)
            for i in xrange(size):
                self.mem_a_with_priv_set(BitArray(uint=address.uint + i, length=32), 1, privileged, False,
                                         value[value.len - 8 - 8 * i:value.len - 8 * i])

    def mem_u_with_priv_get(self, address, size, privileged):
        value = BitArray(length=8 * size)
        if ArchVersion() < 7 and not self.core_registers.sctlr.get_a() and not self.core_registers.sctlr.get_u():
            address = bits_ops.align(address, size)
        if address == bits_ops.align(address, size):
            value = self.mem_a_with_priv_get(address, size, privileged, True)
        elif (HaveVirtExt() and
              not self.core_registers.is_secure() and
              self.core_registers.current_mode_is_hyp() and
              self.core_registers.hsctlr.get_a()):
            self.alignment_fault(address, False)
        elif not self.core_registers.current_mode_is_hyp() and self.core_registers.sctlr.get_a():
            self.alignment_fault(address, False)
        else:
            for i in xrange(size):
                value[value.len - 8 - 8 * i:value.len - 8 * i] = self.mem_a_with_priv_get(
                    BitArray(uint=address.uint + i, length=32), 1, privileged, False)
            if self.core_registers.get_cpsr_e() == "1":
                value = self.big_endian_reverse(value, size)
        return value

    def mem_u_unpriv_get(self, address, size):
        return self.mem_u_with_priv_get(address, size, False)

    def mem_u_unpriv_set(self, address, size, value):
        self.mem_u_with_priv_set(address, size, False, value)

    def mem_u_get(self, address, size):
        return self.mem_u_with_priv_get(address, size, self.core_registers.current_mode_is_not_user())

    def mem_u_set(self, address, size, value):
        self.mem_u_with_priv_set(address, size, self.core_registers.current_mode_is_not_user(), value)

    def big_endian(self):
        return self.core_registers.get_cpsr_e() == "1"

    def unaligned_support(self):
        return self.core_registers.sctlr.get_u()

    def hint_yield(self):
        # mock
        raise NotImplementedError()
        pass

    def clear_event_register(self):
        self.core_registers.set_event_register(False)

    def event_registered(self):
        return self.core_registers.get_event_register()

    def send_event_local(self):
        self.core_registers.set_event_register(True)

    def send_event(self):
        # mock
        raise NotImplementedError()

    def wait_for_event(self):
        self.is_wait_for_event = True

    def wait_for_interrupt(self):
        self.is_wait_for_interrupt = True

    def integer_zero_divide_trapping_enabled(self):
        return is_armv7r_profile() and self.core_registers.sctlr.get_dz()

    def generate_integer_zero_divide(self):
        raise UndefinedInstructionException("division by zero in the integer division instruction")
        pass

    def generate_coprocessor_exception(self):
        raise UndefinedInstructionException("rejected coprocessor instruction")

    def call_supervisor(self, immediate):
        if (self.core_registers.current_mode_is_hyp() or
                (HaveVirtExt() and
                    not self.core_registers.is_secure() and
                    not self.core_registers.current_mode_is_not_user() and
                    self.core_registers.hcr.get_tge())):
            hsr_string = bits_ops.zeros(25)
            hsr_string[9:25] == immediate if self.current_cond() == "0b1110" else BitArray(length=16)  # unknown
            self.write_hsr(BitArray(bin="010001"), hsr_string)
        raise SVCException()

    def cpx_instr_decode(self, instr):
        # mock
        raise NotImplementedError()

    def cp15_instr_decode(self, instr):
        # mock
        raise NotImplementedError()

    def cp14_debug_instr_decode(self, instr):
        # mock
        raise NotImplementedError()

    def cp14_trace_instr_decode(self, instr):
        # mock
        raise NotImplementedError()

    def cp14_jazelle_instr_decode(self, instr):
        # mock
        raise NotImplementedError()

    def instr_is_pl0_undefined(self, instr):
        # mock
        raise NotImplementedError()

    def coproc_accepted(self, cp_num, instr):
        assert cp_num not in (10, 11)
        if cp_num not in (14, 15):
            if HaveSecurityExt():
                if not self.core_registers.is_secure() and not self.core_registers.nsacr.get_cp_n(cp_num):
                    raise UndefinedInstructionException()
            if not HaveVirtExt() or not self.core_registers.current_mode_is_hyp():
                if self.core_registers.cpacr.get_cp_n(cp_num) == "0b00":
                    raise UndefinedInstructionException()
                elif self.core_registers.cpacr.get_cp_n(cp_num) == "0b01":
                    if not self.core_registers.current_mode_is_not_user():
                        raise UndefinedInstructionException()
                elif self.core_registers.cpacr.get_cp_n(cp_num) == "0b10":
                    print "unpredictable"
                elif self.core_registers.cpacr.get_cp_n(cp_num) == "0b11":
                    pass
            if HaveSecurityExt() and HaveVirtExt() and not self.core_registers.is_secure() and \
                    self.core_registers.hcptr.get_tcp_n(cp_num):
                hsr_string = bits_ops.zeros(25)
                hsr_string[21:25] = BitArray(uint=(cp_num & 0xF), length=4)
                self.write_hsr(BitArray(bin="000111"), hsr_string)
                if not self.core_registers.current_mode_is_hyp():
                    self.core_registers.take_hyp_trap_exception()
                else:
                    raise UndefinedInstructionException()
            return self.cpx_instr_decode(instr)
        elif cp_num == 14:
            opc1 = -1
            two_reg = False
            if instr[4:8] == "0b1110" and instr[27] and instr[0:4] != "0b1111":
                opc1 = instr[8:11].uint
                two_reg = False
                if instr[16:20] == "0b1111" and not (instr[8:16] == "0b00010000" and instr[24:32] == "0b00010001"):
                    print "unpredictable"
            elif instr[4:12] == "0b11000101" and instr[0:4] != "0b1111":
                opc1 = instr[24:28].uint
                if opc1 != 0:
                    raise UndefinedInstructionException()
                two_reg = True
            elif instr[4:7] == "0b110" and instr[0:4] != "0b1111" and not instr[9]:
                opc1 = 0
                if instr[16:20].uint != 5:
                    raise UndefinedInstructionException()
            else:
                raise UndefinedInstructionException()
            if opc1 == 0:
                return self.cp14_debug_instr_decode(instr)
            elif opc1 == 1:
                return self.cp14_trace_instr_decode(instr)
            elif opc1 == 6:
                if two_reg:
                    raise UndefinedInstructionException()
                if instr[24:27] != "0b000" or instr[28:31] != "0b000" or instr[16:20] == "0b1111":
                    print "unpredictable"
                else:
                    if not instr[31]:
                        if not self.core_registers.current_mode_is_not_user():
                            raise UndefinedInstructionException()
                    if instr[30]:
                        if not self.core_registers.current_mode_is_not_user() and self.core_registers.teecr.get_xed():
                            raise UndefinedInstructionException()
                    if (HaveSecurityExt() and
                            HaveVirtExt() and
                            not self.core_registers.is_secure() and
                            not self.core_registers.current_mode_is_hyp() and
                            self.core_registers.hstr.get_ttee()):
                        hsr_string = bits_ops.zeros(25)
                        hsr_string[5:8] = instr[24:27]
                        hsr_string[8:11] = instr[8:11]
                        hsr_string[11:15] = instr[12:16]
                        hsr_string[16:20] = instr[16:20]
                        hsr_string[20:24] = instr[28:32]
                        hsr_string[24] = instr[11]
                        self.write_hsr(BitArray(bin="000101"), hsr_string)
                        self.core_registers.take_hyp_trap_exception()
                return True
            elif opc1 == 7:
                return self.cp14_jazelle_instr_decode(instr)
            else:
                raise UndefinedInstructionException()
        elif cp_num == 15:
            cr_nnum = -1
            two_reg = False
            if instr[4:8] == "0b1110" and instr[27] and instr[0:4] != "0b1111":
                cr_nnum = instr[12:16].uint
                two_reg = False
                if instr[16:20] == "0b1111":
                    print "unpredictable"
            elif instr[4:11] == "0b1100010" and instr[0:4] != "0b1111":
                cr_nnum = instr[28:32].uint
                two_reg = True
            else:
                raise UndefinedInstructionException()
            if cr_nnum == 4:
                print "unpredictable"
            if (HaveSecurityExt() and
                    HaveVirtExt() and
                    not self.core_registers.is_secure() and
                    not self.core_registers.current_mode_is_hyp() and
                    cr_nnum != 14 and
                    self.core_registers.hstr.get_t_n(cr_nnum)):
                if not self.core_registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
                    if implementation_defined.coproc_accepted_pl0_undefined:
                        raise UndefinedInstructionException()
                hsr_string = bits_ops.zeros(25)
                if two_reg:
                    hsr_string[5:9] = instr[24:28]
                    hsr_string[11:15] = instr[12:16]
                    hsr_string[16:20] = instr[16:20]
                    hsr_string[20:24] = instr[28:32]
                    hsr_string[24] = instr[11]
                    self.write_hsr(BitArray(bin="000100"), hsr_string)
                else:
                    hsr_string[5:8] = instr[24:27]
                    hsr_string[8:11] = instr[8:11]
                    hsr_string[11:15] = instr[12:16]
                    hsr_string[16:20] = instr[16:20]
                    hsr_string[20:24] = instr[28:32]
                    hsr_string[24] = instr[11]
                    self.write_hsr(BitArray(bin="000011"), hsr_string)
                self.core_registers.take_hyp_trap_exception()
            if (HaveSecurityExt() and
                    HaveVirtExt() and
                    not self.core_registers.is_secure() and
                    not self.core_registers.current_mode_is_hyp() and
                    self.core_registers.hcr.get_tidcp() and
                    not two_reg):
                cr_mnum = instr[28:32].uint
                if (cr_nnum == 9 and cr_mnum in (0, 1, 2, 5, 6, 7, 8)) or (
                        cr_nnum == 10 and cr_mnum in (0, 1, 4, 8)) or (
                        cr_nnum == 11 and cr_mnum in (0, 1, 2, 3, 4, 5, 6, 7, 8, 15)):
                    if not self.core_registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
                        if implementation_defined.coproc_accepted_pl0_undefined:
                            raise UndefinedInstructionException()
                        hsr_string = bits_ops.zeros(25)
                        hsr_string[5:8] = instr[24:27]
                        hsr_string[8:11] = instr[8:11]
                        hsr_string[11:15] = instr[12:16]
                        hsr_string[16:20] = instr[16:20]
                        hsr_string[20:24] = instr[28:32]
                        hsr_string[24] = instr[11]
                        self.write_hsr(BitArray(bin="000011"), hsr_string)
                        self.core_registers.take_hyp_trap_exception()
            return self.cp15_instr_decode(instr)

    def coproc_get_word_to_store(self, cp_num, instr):
        # mock
        raise NotImplementedError()
        pass

    def coproc_done_storing(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_done_loading(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_send_loaded_word(self, word, cp_num, instr):
        # mock
        raise NotImplementedError()
        pass

    def coproc_send_two_words(self, word2, word1, cp_num, instr):
        # mock
        raise NotImplementedError()
        pass

    def coproc_get_two_words(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_internal_operation(self, cp_num, instr):
        # mock
        raise NotImplementedError()
        pass

    def coproc_send_one_word(self, word, cp_num, instr):
        # mock
        raise NotImplementedError()
        pass

    def coproc_get_one_word(self, cp_num, instr):
        # mock
        # CRm = instr[28:32]
        # opc2 = instr[24:27]
        # CRn = instr[12:16]
        # opc1 = instr[8:11]
        # registers_attr = self.core_registers.coproc_register_name(cp_num, CRn, opc1, CRm, opc2)
        # if registers_attr and hasattr(self.core_registers, registers_attr):
        #     return getattr(self.core_registers, registers_attr)
        # return BitArray(length=32)
        raise NotImplementedError()

    def hint_preload_data_for_write(self, address):
        # mock
        raise NotImplementedError()
        pass

    def hint_preload_data(self, address):
        # mock
        raise NotImplementedError()
        pass

    def data_synchronization_barrier(self, domain, types):
        # mock
        raise NotImplementedError()
        pass

    def instruction_synchronization_barrier(self):
        # mock
        raise NotImplementedError()
        pass

    def it_advance(self):
        if self.core_registers.get_cpsr_itstate()[5:8] == "000":
            self.core_registers.set_cpsr_itstate(BitArray(bin="00000000"))
        else:
            it_state = BitArray(bin=self.core_registers.get_cpsr_itstate()[0:4])
            it_state += shift.lsl(BitArray(bin=self.core_registers.get_cpsr_itstate()[4:8]), 1)
            self.core_registers.set_cpsr_itstate(it_state)

    def in_it_block(self):
        return self.core_registers.get_cpsr_itstate()[4:8] != "0000"

    def last_in_it_block(self):
        return self.core_registers.get_cpsr_itstate()[4:8] == "1000"

    def increment_pc_if_needed(self):
        if not self.core_registers.changed_registers[15]:
            self.core_registers.increment_pc(self.this_instr_length() / 8)

    def emulate_cycle(self):
        instr = self.fetch_instruction()
        try:
            opcode_c = self.decode_instruction(instr)
            if not opcode_c:
                raise UndefinedInstructionException()
            opcode_c = opcode_c.from_bitarray(instr, self)
            self.execute_instruction(opcode_c)
            self.increment_pc_if_needed()
        except EndOfInstruction:
            pass
        except SVCException:
            self.take_svc_exception()
        except SMCException:
            self.take_smc_exception()
        except DataAbortException:
            self.take_data_abort_exception()
        except HypTrapException:
            self.take_hyp_trap_exception()
        except UndefinedInstructionException:
            self.take_undef_instr_exception()

    def fetch_instruction(self):
        if self.core_registers.current_instr_set() == InstrSet.InstrSet_ARM:
            self.opcode = self.mem_a_get(self.core_registers.pc_store_value(), 4)
        elif self.core_registers.current_instr_set() == InstrSet.InstrSet_Thumb:
            self.opcode = self.mem_a_get(self.core_registers.pc_store_value(), 2)
            if self.opcode[0:5] == "0b11101" or self.opcode[0:5] == "0b11110" or self.opcode[0:5] == "0b11111":
                self.opcode += self.mem_a_get(
                    bits_ops.add(self.core_registers.pc_store_value(), BitArray(bin="10"), 32), 2)
        return self.opcode

    def decode_instruction(self, instr):
        return opcodes.decode_instruction(instr, self)

    def execute_instruction(self, opcode):
        self.core_registers.changed_registers = [False] * 16
        opcode.execute(self)
