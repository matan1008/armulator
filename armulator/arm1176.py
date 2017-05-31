from bitstring import BitArray
from enum import Enum
from configurations import *
import shift
import bits_ops
import implementation_defined
from arm_exceptions import *
from memory_attributes import MemoryAttributes, MemType
from address_descriptor import AddressDescriptor
from tlb_record import TLBRecord
from memory import Memory
from permissions import Permissions
from enums import *
import opcodes
from armulator.registers import Registers


class ARM1176:
    def __init__(self):
        self.registers = Registers()
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

    def print_registers(self):
        print "{0}:{1}".format("R0", self.registers.get(0))
        print "{0}:{1}".format("R1", self.registers.get(1))
        print "{0}:{1}".format("R2", self.registers.get(2))
        print "{0}:{1}".format("R3", self.registers.get(3))
        print "{0}:{1}".format("R4", self.registers.get(4))
        print "{0}:{1}".format("R5", self.registers.get(5))
        print "{0}:{1}".format("R6", self.registers.get(6))
        print "{0}:{1}".format("R7", self.registers.get(7))
        print "{0}:{1}".format("R8", self.registers.get(8))
        print "{0}:{1}".format("R9", self.registers.get(9))
        print "{0}:{1}".format("R10", self.registers.get(10))
        print "{0}:{1}".format("R11", self.registers.get(11))
        print "{0}:{1}".format("R12", self.registers.get(12))
        print "{0}:{1}".format("SP", self.registers.get_sp())
        print "{0}:{1}".format("LR", self.registers.get_lr())
        print "{0}:{1}".format("PC", self.registers.pc_store_value())
        print "{0}:{1}".format("CPSR", self.registers.cpsr.value)
        # print "{0}:{1}".format(, self.registers.)
        # print "{0}:{1}".format(, self.registers.)

    def take_reset(self):
        self.registers.cpsr.set_m("0b10011")
        if HaveSecurityExt():
            self.registers.scr.set_ns(False)
        self.registers.reset_control_registers()
        if HaveAdvSIMDorVFP():
            self.registers.fpexc.set_en(False)
        if HaveThumbEE():
            self.registers.teecr.set_xed(False)
        if HaveJazelle():
            self.registers.jmcr.set_je(False)
        self.registers.cpsr.set_i(True)
        self.registers.cpsr.set_f(True)
        self.registers.cpsr.set_a(True)
        self.registers.cpsr.set_it(BitArray(length=8))
        self.registers.cpsr.set_j(False)
        self.registers.cpsr.set_t(self.registers.sctlr.get_te())
        self.registers.cpsr.set_e(self.registers.sctlr.get_ee())
        reset_vector = (implementation_defined.impdef_reset_vector
                        if HasIMPDEFResetVactor()
                        else self.registers.exc_vector_base())
        reset_vector[31] = False
        self.registers.branch_to(reset_vector)

    def take_hyp_trap_exception(self):
        preferred_exceptn_return = BitArray(uint=(self.registers.get_pc().uint - 4
                                                  if self.registers.cpsr.get_t()
                                                  else self.registers.get_pc().uint - 8),
                                            length=32)
        new_spsr_value = self.registers.cpsr.value
        self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)

    def take_smc_exception(self):
        self.registers.it_advance()
        new_lr_value = self.registers.get_pc() if self.registers.cpsr.get_t() else BitArray(
            uint=(self.registers.get_pc().uint - 4), length=32)
        new_spsr_value = self.registers.cpsr.value
        vect_offset = 8
        if self.registers.cpsr.get_m() == "0b10110":
            self.registers.scr.set_ns(False)
        self.registers.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)

    def take_data_abort_exception(self):
        new_lr_value = BitArray(uint=self.registers.get_pc().uint + 4,
                                length=32) if self.registers.cpsr.get_t() else self.registers.get_pc()
        new_spsr_value = self.registers.cpsr.value
        vect_offset = 16
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - 8), length=32)
        route_to_monitor = (HaveSecurityExt() and
                            self.registers.scr.get_ea() and
                            self.registers.is_external_abort())
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.registers.scr.get_ns() and
                       self.registers.cpsr.get_m() == "0b11010")
        route_to_hyp = (
            HaveVirtExt() and
            HaveSecurityExt() and
            not self.registers.is_secure() and
            (
                self.registers.second_stage_abort() or
                (
                    self.registers.cpsr.get_m() != "0b11010" and
                    (
                        self.registers.is_external_abort() and
                        self.registers.is_async_abort() and
                        self.registers.hcr.get_amo()
                    ) or
                    (
                        self.registers.debug_exception() and
                        self.registers.hdcr.get_tde()
                    )
                ) or
                (
                    self.registers.cpsr.get_m() == "0b10000" and
                    self.registers.hcr.get_tge() and
                    (
                        self.registers.is_alignment_fault() or
                        (
                            self.registers.is_external_abort() and
                            not self.registers.is_async_abort()
                        )
                    )
                )
            )
        )
        if route_to_monitor:
            if self.registers.cpsr.get_m() == "0b10110":
                self.registers.scr.set_ns(False)
            self.registers.enter_monitor_mode(new_spsr_value, new_lr_value, vect_offset)
        elif take_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if HaveSecurityExt() and self.registers.cpsr.get_m() == "0b10110":
                self.registers.scr.set_ns(False)
            self.registers.cpsr.set_m("0b10111")
            self.registers.set_spsr(new_spsr_value)
            self.registers.set(14, new_lr_value)
            self.registers.cpsr.set_i(True)
            if (not HaveSecurityExt() or
                    HaveVirtExt() or
                    not self.registers.scr.get_ns() or
                    self.registers.scr.get_aw()):
                self.registers.cpsr.set_a(True)
            self.registers.cpsr.set_it(BitArray(length=8))
            self.registers.cpsr.set_j(False)
            self.registers.cpsr.set_t(self.registers.sctlr.get_te())
            self.registers.cpsr.set_e(self.registers.sctlr.get_ee())
            self.registers.branch_to(
                BitArray(uint=(self.registers.exc_vector_base().uint + vect_offset), length=32))

    def take_svc_exception(self):
        self.registers.it_advance()
        new_lr_value = bits_ops.sub(self.registers.get_pc(), BitArray(bin="10"),
                                    32) if self.registers.cpsr.get_t() else bits_ops.sub(
            self.registers.get_pc(), BitArray(bin="100"), 32)
        new_spsr_value = self.registers.cpsr.value
        vect_offset = 8
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.registers.scr.get_ns() and
                       self.registers.cpsr.get_m() == "0b11010")
        route_to_hyp = (HaveVirtExt() and
                        HaveSecurityExt() and
                        not self.registers.is_secure() and
                        self.registers.hcr.get_tge() and
                        self.registers.cpsr.get_m() == "0b10000")
        preferred_exceptn_return = new_lr_value
        if take_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.registers.cpsr.get_m() == "0b10110":
                self.registers.scr.set_ns(False)
            self.registers.cpsr.set_m("0b10011")
            self.registers.set_spsr(new_spsr_value)
            self.registers.set(14, new_lr_value)
            self.registers.cpsr.set_i(True)
            self.registers.cpsr.set_it(BitArray(length=8))
            self.registers.cpsr.set_j(False)
            self.registers.cpsr.set_t(self.registers.sctlr.get_te())
            self.registers.cpsr.set_e(self.registers.sctlr.get_ee())
            self.registers.branch_to(
                bits_ops.add(self.registers.exc_vector_base(), BitArray(uint=vect_offset, length=32), 32))

    def take_undef_instr_exception(self):
        new_lr_value = BitArray(uint=(self.registers.get_pc().uint - 2),
                                length=32) if self.registers.cpsr.get_t() else BitArray(
            uint=(self.registers.get_pc().uint - 4), length=32)
        new_spsr_value = self.registers.cpsr.value
        vect_offset = 4
        take_to_hyp = (HaveVirtExt() and
                       HaveSecurityExt() and
                       self.registers.scr.get_ns() and
                       self.registers.cpsr.get_m() == "0b11010")
        route_to_hyp = (HaveVirtExt() and
                        HaveSecurityExt() and
                        not self.registers.is_secure() and
                        self.registers.hcr.get_tge() and
                        self.registers.cpsr.get_m() == "0b10000")
        return_offset = 2 if self.registers.cpsr.get_t() else 4
        preferred_exceptn_return = BitArray(uint=(new_lr_value.uint - return_offset), length=32)
        if take_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, vect_offset)
        elif route_to_hyp:
            self.registers.enter_hyp_mode(new_spsr_value, preferred_exceptn_return, 20)
        else:
            if self.registers.cpsr.get_m() == "0b10110":
                self.registers.scr.set_ns(False)
            self.registers.cpsr.set_m("0b11011")
            self.registers.set_spsr(new_spsr_value)
            self.registers.set(14, new_lr_value)
            self.registers.cpsr.set_i(True)
            self.registers.cpsr.set_it(BitArray(length=8))
            self.registers.cpsr.set_j(False)
            self.registers.cpsr.set_t(self.registers.sctlr.get_te())
            self.registers.cpsr.set_e(self.registers.sctlr.get_ee())
            self.registers.branch_to(
                BitArray(uint=(self.registers.exc_vector_base().uint + vect_offset), length=32))

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
        if self.registers.current_instr_set() == InstrSet.InstrSet_ARM:
            result = self.opcode[0:4]
        elif self.opcode.length == 16 and self.opcode.bin[0:4] == "1101":
            result = self.opcode[4:8]
        elif self.opcode.length == 32 and self.opcode.bin[0:5] == "11110" and self.opcode.bin[16:18] == "10" and not \
                self.opcode[19]:
            result = self.opcode[6:10]
        else:
            if self.registers.cpsr.get_it()[4:8] != "0b0000":
                result = self.registers.cpsr.get_it()[0:4]
            elif self.registers.cpsr.get_it() == "0b00000000":
                result = BitArray(bin="1110")
            else:
                print "unpredictable"
        return result

    def condition_passed(self):
        cond = self.current_cond()
        if cond.bin[0:3] == "000":
            result = self.registers.cpsr.get_z()
        elif cond.bin[0:3] == "001":
            result = self.registers.cpsr.get_c()
        elif cond.bin[0:3] == "010":
            result = self.registers.cpsr.get_n()
        elif cond.bin[0:3] == "011":
            result = self.registers.cpsr.get_v()
        elif cond.bin[0:3] == "100":
            result = self.registers.cpsr.get_c() and not self.registers.cpsr.get_z()
        elif cond.bin[0:3] == "101":
            result = self.registers.cpsr.get_n() == self.registers.cpsr.get_v()
        elif cond.bin[0:3] == "110":
            result = (self.registers.cpsr.get_n() == self.registers.cpsr.get_v() and
                      not self.registers.cpsr.get_z())
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
            if self.registers.current_instr_set() == InstrSet.InstrSet_ARM:
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
        self.registers.hsr.value = hsr_value

    def switch_to_jazelle_execution(self):
        raise NotImplementedError()

    def branch_write_pc(self, address):
        if self.registers.current_instr_set() == InstrSet.InstrSet_ARM:
            if ArchVersion() < 6 and address.bin[29:] != "00":
                print "unpredictable"
            self.registers.branch_to(address[:-2] + BitArray(bin="00"))
        elif self.registers.current_instr_set() == InstrSet.InstrSet_Jazelle:
            if JazelleAcceptsExecution():
                self.registers.branch_to(address)
            else:
                self.registers.branch_to(address[:-2] + BitArray(bin="00"))
        else:
            address.set(False, 31)
            self.registers.branch_to(address)

    def bx_write_pc(self, address):
        if self.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE:
            if address[31]:
                address.set(False, 31)
                self.registers.branch_to(address)
            else:
                print "unpredictable"
        else:
            if address[31]:
                self.registers.select_instr_set(InstrSet.InstrSet_Thumb)
                address.set(False, 31)
                self.registers.branch_to(address)
            elif not address[30]:
                self.registers.select_instr_set(InstrSet.InstrSet_ARM)
                self.registers.branch_to(address)
            else:
                print "unpredictable"

    def alu_write_pc(self, address):
        if ArchVersion() >= 7 and self.registers.current_instr_set() == InstrSet.InstrSet_ARM:
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
        if self.registers.current_instr_set() == InstrSet.InstrSet_ThumbEE:
            if n == 15:
                if bits_ops.align(self.registers.get_pc(), 4).all(False):
                    print "unpredictable"
            elif n == 13:
                if self.registers.get_sp().all(False):
                    print "unpredictable"
            else:
                if self.registers.get(n).all(False):
                    self.registers.set_lr(self.registers.get_pc()[:-1] + BitArray(bin="1"))
                    self.registers.cpsr.set_it(BitArray(bin="00000000"))
                    self.branch_write_pc(BitArray(uint=(self.registers.teehbr.uint - 4), length=32))
                    raise EndOfInstruction("NullCheckIfThumbEE")

    def fcse_translate(self, va):
        if va.bin[0:7] == "0000000":
            mva = self.registers.fcseidr.get_pid() + va[7:32]
        else:
            mva = va
        return mva

    def default_memory_attributes(self, va):
        memattrs = MemoryAttributes()
        if va[0:2] == "0b00":
            if not self.registers.sctlr.get_c():
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b00"
                memattrs.shareable = True
            else:
                memattrs.type = MemType.MemType_Normal
                memattrs.innerattrs[0:2] = "0b01"
                memattrs.shareable = False
        elif va[0:2] == "0b01":
            if not self.registers.sctlr.get_c() or va[2]:
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
        if self.registers.sctlr.get_afe():
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
        if self.registers.dacr.get_d_n(domain.uint) == "0b00":
            self.data_abort(mva, ipaddress, domain, level, iswrite, self.DAbort.DAbort_Domain, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
        elif self.registers.dacr.get_d_n(domain.uint) == "0b01":
            permission_check = True
        if self.registers.dacr.get_d_n(domain.uint) == "0b10":
            print "unpredictable"
        if self.registers.dacr.get_d_n(domain.uint) == "0b11":
            permission_check = False
        return permission_check

    def second_stage_translate(self, s1_out_addr_desc, mva, size, is_write):
        result = AddressDescriptor()
        tlbrecord_s2 = TLBRecord()
        if HaveVirtExt() and not self.registers.is_secure() and not self.registers.current_mode_is_hyp():
            if self.registers.hcr.get_vm():
                s2ia = s1_out_addr_desc.paddress.physicaladdress
                stage1 = False
                s2fs1walk = True
                tlbrecord_s2 = self.translation_table_walk_ld(s2ia, mva, is_write, stage1, s2fs1walk, size)
                self.check_permission_s2(tlbrecord_s2.perms, mva, s2ia, tlbrecord_s2.level, False, s2fs1walk)
                if self.registers.hcr.get_ptw():
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
                if (dtype in (self.DAbort.DAbort_AsyncParity,
                              self.DAbort.DAbort_AsyncExternal,
                              self.DAbort.DAbort_AsyncWatchpoint) or
                    (dtype == self.DAbort.DAbort_SyncWatchpoint and
                        self.registers.dbgdidr.get_version().uint <= 4)):
                    self.registers.dfar = BitArray(length=32)  # unknown
                else:
                    self.registers.dfar = vaddress
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
                self.registers.dfsr.value[18:32] = dfsr_string
            else:
                hsr_string = BitArray(length=25)
                ec = BitArray(length=6)
                self.registers.hdfar = vaddress
                if ipavalid:
                    self.registers.hpfar.set_fipa(ipaddress[0:28])
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
                        self.registers.dbgdidr.get_version().uint <= 4)):
                self.registers.dfar = BitArray(length=32)  # unknown
            elif dtype == self.DAbort.DAbort_SyncParity:
                if implementation_defined.data_abort_pmsa_change_dfar:
                    self.registers.dfar = vaddress
            else:
                self.registers.dfar = vaddress
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
            self.registers.dfsr.value[18:32] = dfsr_string
        raise DataAbortException()

    def alignment_fault_v(self, address, iswrite, taketohyp, secondstageabort):
        ipaddress = BitArray(length=40)  # unknown
        domain = BitArray(length=4)  # unknown
        level = 0  # unknown
        ipavalid = False
        ldfsr_fromat = taketohyp or self.registers.ttbcr.get_eae()
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
            taketohypmode = self.registers.current_mode_is_hyp() or self.registers.hcr.get_tge()
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
        if self.registers.current_mode_is_hyp():
            mair = self.registers.hmair1 + self.registers.hmair0
        else:
            mair = self.registers.mair1 + self.registers.mair0
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
            if self.registers.prrr.get_tr_n(region) == "0b00":
                memattrs.type = MemType.MemType_StronglyOrdered
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.registers.prrr.get_tr_n(region) == "0b01":
                memattrs.type = MemType.MemType_Device
                memattrs.innerattrs = BitArray(length=2)  # unknown
                memattrs.outerattrs = BitArray(length=2)  # unknown
                memattrs.innerhints = BitArray(length=2)  # unknown
                memattrs.outerhints = BitArray(length=2)  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.registers.prrr.get_tr_n(region) == "0b10":
                memattrs.type = MemType.MemType_Normal
                hintsattrs = self.convert_attrs_hints(self.registers.nmrr.get_ir_n(region))
                memattrs.innerattrs = hintsattrs[2:4]
                memattrs.innerhints = hintsattrs[0:2]
                hintsattrs = self.convert_attrs_hints(self.registers.nmrr.get_or_n(region))
                memattrs.outerattrs = hintsattrs[2:4]
                memattrs.outerhints = hintsattrs[0:2]
                s_bit = self.registers.prrr.get_ns0() if not s else self.registers.prrr.get_ns1()
                memattrs.shareable = s_bit
                memattrs.outershareable = s_bit and not self.registers.prrr.get_nos_n(region)
            elif self.registers.prrr.get_tr_n(region) == "0b11":
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
            if self.registers.current_mode_is_hyp():
                lookup_secure = False
                t0_size = self.registers.htcr.get_t0sz().uint
                if t0_size == 0 or ia[8:t0_size + 8].uint == 0:
                    current_level = 1 if self.registers.htcr.get_t0sz()[0:2] == "0b00" else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = self.registers.httbr[24:64 - ba_lower_bound] + BitArray(length=ba_lower_bound)
                    if self.registers.httbr[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.registers.htcr.get_irgn0())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.registers.htcr.get_orgn0())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.registers.htcr.get_sh0()[0]
                    walkaddr.memattrs.outershareable = self.registers.htcr.get_sh0() == "0b10"
                    walkaddr.paddress.ns = True
            else:
                lookup_secure = self.registers.is_secure()
                t0_size = self.registers.ttbcr.get_t0sz().uint
                if t0_size == 0 or ia[8:t0_size + 8].uint == 0:
                    current_level = 1 if self.registers.ttbcr.get_t0sz().bin[0:2] == "00" else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = self.registers.ttbr0_64[24:64 - ba_lower_bound] + BitArray(
                        length=ba_lower_bound)
                    if self.registers.ttbr0_64[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    disabled = self.registers.ttbcr.get_epd0()
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.get_irgn0())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.get_orgn0())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.registers.ttbcr.get_sh0()[0]
                    walkaddr.memattrs.outershareable = self.registers.ttbcr.get_sh0() == "0b10"
                t1_size = self.registers.ttbcr.get_t1sz().uint
                if (t1_size == 0 and not base_found) or ia[8:t1_size + 8].all(True):
                    current_level = 1 if self.registers.ttbcr.get_t1sz().bin[0:2] == "00" else 2
                    ba_lower_bound = 9 * current_level - t1_size - 4
                    base_address = self.registers.ttbr1_64[24:64 - ba_lower_bound] + BitArray(
                        length=ba_lower_bound)
                    if self.registers.ttbr1_64[64 - ba_lower_bound:61].uint != 0:
                        print "unpredictable"
                    base_found = True
                    disabled = self.registers.ttbcr.get_epd1()
                    start_bit = 31 - t1_size
                    walkaddr.memattrs.type = MemType.MemType_Normal
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.get_irgn1())
                    walkaddr.memattrs.innerhints = hintsattrs[0:2]
                    walkaddr.memattrs.innerattrs = hintsattrs[2:4]
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.get_orgn1())
                    walkaddr.memattrs.outerhints = hintsattrs[0:2]
                    walkaddr.memattrs.outerattrs = hintsattrs[2:4]
                    walkaddr.memattrs.shareable = self.registers.ttbcr.get_sh1()[0]
                    walkaddr.memattrs.outershareable = self.registers.ttbcr.get_sh1() == "0b10"
        else:
            t0_size = self.registers.vtcr.get_t0sz().uint
            s_level = self.registers.vtcr.get_sl0().uint
            ba_lower_bound = 14 - t0_size - (9 * s_level)
            if s_level == 0 and t0_size < -2:
                print "unpredictable"
            if s_level == 1 and t0_size > 1:
                print "unpredictable"
            if self.registers.vtcr.get_sl0()[0]:
                print "unpredictable"
            if self.registers.vttbr[64 - ba_lower_bound:61].uint != 0:
                print "unpredictable"
            if t0_size == -8 or ia[0:t0_size + 8].uint == 0:
                current_level = 2 - s_level
                base_address = self.registers.vttbr[24:64 - ba_lower_bound] + BitArray(length=ba_lower_bound)
                base_found = True
                start_bit = 31 - t0_size
            lookup_secure = False
            walkaddr.memattrs.type = MemType.MemType_Normal
            hintsattrs = self.convert_attrs_hints(self.registers.vtcr.get_irgn0())
            walkaddr.memattrs.innerhints = hintsattrs[0:2]
            walkaddr.memattrs.innerattrs = hintsattrs[2:4]
            hintsattrs = self.convert_attrs_hints(self.registers.vtcr.get_orgn0())
            walkaddr.memattrs.outerhints = hintsattrs[0:2]
            walkaddr.memattrs.outerattrs = hintsattrs[2:4]
            walkaddr.memattrs.shareable = self.registers.vtcr.get_sh0()[0]
            walkaddr.memattrs.outershareable = self.registers.vtcr.get_sh0() == "0b10"
        if not base_found or disabled:
            taketohypmode = self.registers.current_mode_is_hyp() or not stage1
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
            if not HaveVirtExt() or not stage1 or self.registers.is_secure() or self.registers.current_mode_is_hyp():
                if HaveVirtExt() and (self.registers.current_mode_is_hyp() or not stage1):
                    big_endian = self.registers.hsctlr.get_ee()
                else:
                    big_endian = self.registers.sctlr.get_ee()
                descriptor = self.mem[walkaddr, 8]
                if big_endian:
                    descriptor = self.big_endian_reverse(descriptor, 8)
            else:
                walkaddr2 = self.second_stage_translate(walkaddr, ia[8:40], 8, is_write)
                descriptor = self.mem[walkaddr2, 8]
                if self.registers.sctlr.get_ee():
                    descriptor = self.big_endian_reverse(descriptor, 8)
            if not descriptor[-1]:
                taketohypmode = self.registers.current_mode_is_hyp() or not stage1
                ipavalid = not stage1
                self.data_abort(va, ia, domain, current_level, is_write, self.DAbort.DAbort_Translation, taketohypmode,
                                not stage1, ipavalid, ldfsr_format, s2fs1walk)
            else:
                if not descriptor[-2]:
                    if current_level == 3:
                        taketohypmode = self.registers.current_mode_is_hyp() or not stage1
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
                    if self.registers.is_secure() and not lookup_secure:
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
            taketohypmode = self.registers.current_mode_is_hyp() or not stage1
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
        if stage1 and self.registers.current_mode_is_hyp():
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
        n = self.registers.ttbcr.get_n().uint
        if n == 0 or mva[0:n + 1].uint == 0:
            ttbr = self.registers.ttbr0_64
            disabled = self.registers.ttbcr.get_pd1()
        else:
            ttbr = self.registers.ttbr1_64
            disabled = self.registers.ttbcr.get_pd1()
            n = 0
        if HaveSecurityExt() and disabled:
            level = 1
            self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, stage2,
                            ipavalid, ldfsr_format, s2fs1walk)
        l1descaddr.paddress.physicaladdress = "0b00000000" + ttbr[32:n + 50] + mva[n:12] + "0b00"
        l1descaddr.paddress.ns = not self.registers.is_secure()
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
        if not HaveVirtExt() or self.registers.is_secure():
            l1descaddr2 = l1descaddr
        else:
            l1descaddr2 = self.second_stage_translate(l1descaddr, mva, 4, is_write)
        l1desc = self.mem[l1descaddr2, 4]
        if self.registers.sctlr.get_ee():
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
            l2descaddr.paddress.ns = not self.registers.is_secure()
            l2descaddr.memattrs = l1descaddr.memattrs
            if not HaveVirtExt() or self.registers.is_secure():
                l2descaddr2 = l2descaddr
            else:
                l2descaddr2 = self.second_stage_translate(l2descaddr, mva, 4, is_write)
            l2desc = self.mem[l2descaddr2, 4]
            if self.registers.sctlr.get_ee():
                l2desc = self.big_endian_reverse(l2desc, 4)
            if l2desc[30:32] == "0b00":
                self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_Translation, taketohypmode, stage2,
                                ipavalid, ldfsr_format, s2fs1walk)
            s = l2desc[21]
            ap = l2desc[22:23] + l2desc[26:28]
            ng = l2desc[20]
            if self.registers.sctlr.get_afe() and not l2desc[27]:
                if not self.registers.sctlr.get_ha():
                    self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_AccessFlag, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.registers.sctlr.get_ee():
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
            if self.registers.sctlr.get_afe() and not l1desc[21]:
                if not self.registers.sctlr.get_ha():
                    self.data_abort(mva, ia, domain, level, is_write, self.DAbort.DAbort_AccessFlag, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.registers.sctlr.get_ee():
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
        if not self.registers.sctlr.get_tre():
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
        result.addrdesc.paddress.ns = ns if self.registers.is_secure() else True
        return result

    def translate_address_v_s1_off(self, va):
        result = TLBRecord()
        if (not HaveVirtExt() or
                not self.registers.hcr.get_dc() or
                self.registers.is_secure() or
                self.registers.current_mode_is_hyp()):
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
            if not self.registers.hcr.get_vm():
                print "unpredictable"
        result.perms.ap = BitArray(length=3)  # unknown
        result.perms.xn = False
        result.perms.pxn = False
        result.ng = False  # unknown
        result.domain = BitArray(length=4)  # unknown
        result.level = 0  # unknown
        result.blocksize = 0  # unknown
        result.addrdesc.paddress.physicaladdress = "0b00000000" + va
        result.addrdesc.paddress.ns = not self.registers.is_secure()
        return result

    def translate_address_v(self, va, ispriv, iswrite, size, wasaligned):
        result = AddressDescriptor()
        s2fs1walk = False
        mva = self.fcse_translate(va)
        ishyp = self.registers.current_mode_is_hyp()
        if (ishyp and self.registers.hsctlr.get_m()) or (not ishyp and self.registers.sctlr.get_m()):
            if (HaveVirtExt() and
                    not self.registers.is_secure() and
                    not ishyp and
                    self.registers.hcr.get_tge()):
                print "unpredictable"
            uses_ld = ishyp or self.registers.ttbcr.get_eae()
            if uses_ld:
                ia_in = BitArray(bin="00000000") + mva
                tlbrecord_s1 = self.translation_table_walk_ld(ia_in, mva, iswrite, True, s2fs1walk, size)
                check_domain = False
                check_permission = True
            else:
                tlbrecord_s1 = self.translation_table_walk_sd(mva, iswrite, size)
                check_domain = True
                check_permission = True
        else:
            tlbrecord_s1 = self.translate_address_v_s1_off(mva)
            check_domain = False
            check_permission = False
        if (not wasaligned and
                tlbrecord_s1.addrdesc.memattrs.type in (MemType.MemType_StronglyOrdered, MemType.MemType_Device)):
            if not HaveVirtExt():
                print "unpredictable"
            secondstageabort = False
            self.alignment_fault_v(mva, iswrite, ishyp, secondstageabort)
        if check_domain:
            check_permission = self.check_domain(tlbrecord_s1.domain, mva, tlbrecord_s1.level, iswrite)
        if check_permission:
            self.check_permission(
                tlbrecord_s1.perms, mva, tlbrecord_s1.level, tlbrecord_s1.domain, iswrite, ispriv, ishyp, uses_ld
            )
        if HaveVirtExt() and not self.registers.is_secure() and not ishyp:
            if self.registers.hcr.get_vm():
                s1outputaddr = tlbrecord_s1.addrdesc.paddress.physicaladdress
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
                result = self.combine_s1s2_desc(tlbrecord_s1.addrdesc, tlbrecordS2.addrdesc)
            else:
                result = tlbrecord_s1.addrdesc
        else:
            result = tlbrecord_s1.addrdesc
        return result

    def translate_address_p(self, va, ispriv, iswrite, wasaligned):
        result = AddressDescriptor()
        perms = Permissions
        result.paddress.physicaladdress = "0b00000000" + va
        # IMPLEMENTATION_DEFINED setting of result.paddress.NS;
        if not self.registers.sctlr.get_m():
            result.memattrs = self.default_memory_attributes(va)
        else:
            region_found = False
            texcb = BitArray(length=5)  # unknown
            s = False  # unknown
            for r in xrange(self.registers.mpuir.get_dregion().uint):
                size_enable = self.registers.drsrs[r]
                base_address = self.registers.drbars[r]
                access_control = self.registers.dracrs[r]
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
                if not self.registers.sctlr.get_br() or not ispriv:
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
                    perms.xn = not self.registers.sctlr.get_v() if va[0:4] == "0b1111" else va[0]
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
            memaddrdesc = self.translate_address(address, self.registers.current_mode_is_not_user(), True, size,
                                                 True)
        passed = self.is_exclusive_local(memaddrdesc.paddress, ProcessorID(), size)
        if passed:
            self.clear_exclusive_local(ProcessorID())
        if memaddrdesc.memattrs.shareable:
            passed = passed and self.is_exclusive_global(memaddrdesc.paddress, ProcessorID(), size)
        return passed

    def set_exclusive_monitors(self, address, size):
        memaddrdesc = self.translate_address(address, self.registers.current_mode_is_not_user(), False, size, True)
        if memaddrdesc.memattrs.shareable:
            self.mark_exclusive_global(memaddrdesc.paddress, ProcessorID(), size)
        self.mark_exclusive_local(memaddrdesc.paddress, ProcessorID(), size)

    def mem_a_with_priv_set(self, address, size, privileged, was_aligned, value):
        if address == bits_ops.align(address, size):
            va = address
        elif ArchVersion() >= 7 or self.registers.sctlr.get_a() or self.registers.sctlr.get_u():
            self.alignment_fault(address, True)
        else:
            va = bits_ops.align(address, size)
        memaddrdesc = self.translate_address(va, privileged, True, size, was_aligned)
        if memaddrdesc.memattrs.shareable:
            self.clear_exclusive_by_address(memaddrdesc.paddress, ProcessorID(), size)
        if self.registers.cpsr.get_e():
            value = self.big_endian_reverse(value, size)
        self.mem[memaddrdesc, size] = value

    def mem_a_with_priv_get(self, address, size, privileged, was_aligned):
        if address == bits_ops.align(address, size):
            va = address
        elif ArchVersion() >= 7 or self.registers.sctlr.get_a() or self.registers.sctlr.get_u():
            self.alignment_fault(address, False)
        else:
            va = bits_ops.align(address, size)
        memaddrdesc = self.translate_address(va, privileged, False, size, was_aligned)
        value = self.mem[memaddrdesc, size]
        if self.registers.cpsr.get_e():
            value = self.big_endian_reverse(value, size)
        return value

    def mem_a_set(self, address, size, value):
        self.mem_a_with_priv_set(address, size, self.registers.current_mode_is_not_user(), True, value)

    def mem_a_get(self, address, size):
        return self.mem_a_with_priv_get(address, size, self.registers.current_mode_is_not_user(), True)

    def mem_u_with_priv_set(self, address, size, privileged, value):
        if ArchVersion() < 7 and not self.registers.sctlr.get_a() and not self.registers.sctlr.get_u():
            address = bits_ops.align(address, size)
        if address == bits_ops.align(address, size):
            self.mem_a_with_priv_set(address, size, privileged, True, value)
        elif (HaveVirtExt() and
                not self.registers.is_secure() and
                self.registers.current_mode_is_hyp() and
                self.registers.hsctlr.get_a()):
            self.alignment_fault(address, True)
        elif not self.registers.current_mode_is_hyp() and self.registers.sctlr.get_a():
            self.alignment_fault(address, True)
        else:
            if self.registers.cpsr.get_e():
                value = self.big_endian_reverse(value, size)
            for i in xrange(size):
                self.mem_a_with_priv_set(BitArray(uint=address.uint + i, length=32), 1, privileged, False,
                                         value[value.len - 8 - 8 * i:value.len - 8 * i])

    def mem_u_with_priv_get(self, address, size, privileged):
        value = BitArray(length=8 * size)
        if ArchVersion() < 7 and not self.registers.sctlr.get_a() and not self.registers.sctlr.get_u():
            address = bits_ops.align(address, size)
        if address == bits_ops.align(address, size):
            value = self.mem_a_with_priv_get(address, size, privileged, True)
        elif (HaveVirtExt() and
              not self.registers.is_secure() and
              self.registers.current_mode_is_hyp() and
              self.registers.hsctlr.get_a()):
            self.alignment_fault(address, False)
        elif not self.registers.current_mode_is_hyp() and self.registers.sctlr.get_a():
            self.alignment_fault(address, False)
        else:
            for i in xrange(size):
                value[value.len - 8 - 8 * i:value.len - 8 * i] = self.mem_a_with_priv_get(
                    BitArray(uint=address.uint + i, length=32), 1, privileged, False)
            if self.registers.cpsr.get_e():
                value = self.big_endian_reverse(value, size)
        return value

    def mem_u_unpriv_get(self, address, size):
        return self.mem_u_with_priv_get(address, size, False)

    def mem_u_unpriv_set(self, address, size, value):
        self.mem_u_with_priv_set(address, size, False, value)

    def mem_u_get(self, address, size):
        return self.mem_u_with_priv_get(address, size, self.registers.current_mode_is_not_user())

    def mem_u_set(self, address, size, value):
        self.mem_u_with_priv_set(address, size, self.registers.current_mode_is_not_user(), value)

    def big_endian(self):
        return self.registers.cpsr.get_e()

    def unaligned_support(self):
        return self.registers.sctlr.get_u()

    def hint_yield(self):
        # mock
        raise NotImplementedError()
        pass

    def clear_event_register(self):
        self.registers.set_event_register(False)

    def event_registered(self):
        return self.registers.get_event_register()

    def send_event_local(self):
        self.registers.set_event_register(True)

    def send_event(self):
        # mock
        raise NotImplementedError()

    def wait_for_event(self):
        self.is_wait_for_event = True

    def wait_for_interrupt(self):
        self.is_wait_for_interrupt = True

    def integer_zero_divide_trapping_enabled(self):
        return is_armv7r_profile() and self.registers.sctlr.get_dz()

    def generate_integer_zero_divide(self):
        raise UndefinedInstructionException("division by zero in the integer division instruction")
        pass

    def generate_coprocessor_exception(self):
        raise UndefinedInstructionException("rejected coprocessor instruction")

    def call_supervisor(self, immediate):
        if (self.registers.current_mode_is_hyp() or
                (HaveVirtExt() and
                    not self.registers.is_secure() and
                    not self.registers.current_mode_is_not_user() and
                    self.registers.hcr.get_tge())):
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
                if not self.registers.is_secure() and not self.registers.nsacr.get_cp_n(cp_num):
                    raise UndefinedInstructionException()
            if not HaveVirtExt() or not self.registers.current_mode_is_hyp():
                if self.registers.cpacr.get_cp_n(cp_num) == "0b00":
                    raise UndefinedInstructionException()
                elif self.registers.cpacr.get_cp_n(cp_num) == "0b01":
                    if not self.registers.current_mode_is_not_user():
                        raise UndefinedInstructionException()
                elif self.registers.cpacr.get_cp_n(cp_num) == "0b10":
                    print "unpredictable"
                elif self.registers.cpacr.get_cp_n(cp_num) == "0b11":
                    pass
            if HaveSecurityExt() and HaveVirtExt() and not self.registers.is_secure() and \
                    self.registers.hcptr.get_tcp_n(cp_num):
                hsr_string = bits_ops.zeros(25)
                hsr_string[21:25] = BitArray(uint=(cp_num & 0xF), length=4)
                self.write_hsr(BitArray(bin="000111"), hsr_string)
                if not self.registers.current_mode_is_hyp():
                    self.registers.take_hyp_trap_exception()
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
                        if not self.registers.current_mode_is_not_user():
                            raise UndefinedInstructionException()
                    if instr[30]:
                        if not self.registers.current_mode_is_not_user() and self.registers.teecr.get_xed():
                            raise UndefinedInstructionException()
                    if (HaveSecurityExt() and
                            HaveVirtExt() and
                            not self.registers.is_secure() and
                            not self.registers.current_mode_is_hyp() and
                            self.registers.hstr.get_ttee()):
                        hsr_string = bits_ops.zeros(25)
                        hsr_string[5:8] = instr[24:27]
                        hsr_string[8:11] = instr[8:11]
                        hsr_string[11:15] = instr[12:16]
                        hsr_string[16:20] = instr[16:20]
                        hsr_string[20:24] = instr[28:32]
                        hsr_string[24] = instr[11]
                        self.write_hsr(BitArray(bin="000101"), hsr_string)
                        self.registers.take_hyp_trap_exception()
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
                    not self.registers.is_secure() and
                    not self.registers.current_mode_is_hyp() and
                    cr_nnum != 14 and
                    self.registers.hstr.get_t_n(cr_nnum)):
                if not self.registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
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
                self.registers.take_hyp_trap_exception()
            if (HaveSecurityExt() and
                    HaveVirtExt() and
                    not self.registers.is_secure() and
                    not self.registers.current_mode_is_hyp() and
                    self.registers.hcr.get_tidcp() and
                    not two_reg):
                cr_mnum = instr[28:32].uint
                if (cr_nnum == 9 and cr_mnum in (0, 1, 2, 5, 6, 7, 8)) or (
                        cr_nnum == 10 and cr_mnum in (0, 1, 4, 8)) or (
                        cr_nnum == 11 and cr_mnum in (0, 1, 2, 3, 4, 5, 6, 7, 8, 15)):
                    if not self.registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
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
                        self.registers.take_hyp_trap_exception()
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
        # registers_attr = self.registers.coproc_register_name(cp_num, CRn, opc1, CRm, opc2)
        # if registers_attr and hasattr(self.registers, registers_attr):
        #     return getattr(self.registers, registers_attr)
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
        if self.registers.cpsr.get_it()[5:8] == "0b000":
            self.registers.cpsr.set_it(BitArray(bin="00000000"))
        else:
            it_state = self.registers.cpsr.get_it()[0:4]
            it_state += shift.lsl(self.registers.cpsr.get_it()[4:8], 1)
            self.registers.cpsr.set_it(it_state)

    def in_it_block(self):
        return self.registers.cpsr.get_it()[4:8] != "0b0000"

    def last_in_it_block(self):
        return self.registers.cpsr.get_it()[4:8] == "0b1000"

    def increment_pc_if_needed(self):
        if not self.registers.changed_registers[15]:
            self.registers.increment_pc(self.this_instr_length() / 8)

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
        if self.registers.current_instr_set() == InstrSet.InstrSet_ARM:
            self.opcode = self.mem_a_get(self.registers.pc_store_value(), 4)
        elif self.registers.current_instr_set() == InstrSet.InstrSet_Thumb:
            self.opcode = self.mem_a_get(self.registers.pc_store_value(), 2)
            if self.opcode[0:5] == "0b11101" or self.opcode[0:5] == "0b11110" or self.opcode[0:5] == "0b11111":
                self.opcode += self.mem_a_get(bits_ops.add(self.registers.pc_store_value(), BitArray(bin="10"), 32), 2)
        return self.opcode

    def decode_instruction(self, instr):
        return opcodes.decode_instruction(instr, self)

    def execute_instruction(self, opcode):
        self.registers.changed_registers = [False] * 16
        opcode.execute(self)
