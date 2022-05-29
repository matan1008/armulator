from os import path

from armulator.armv6.address_descriptor import AddressDescriptor
from armulator.armv6.arm_exceptions import *
from armulator.armv6.bits_ops import substring, chain, bit_at, lower_chunk, set_substring, set_bit_at, align, \
    big_endian_reverse, is_ones, to_signed, add
from armulator.armv6.configurations import *
from armulator.armv6.enums import *
from armulator.armv6.memory_attributes import MemoryAttributes, MemType
from armulator.armv6.memory_controller_hub import MemoryControllerHub
from armulator.armv6.opcodes.abstract_opcodes.ldrbt import Ldrbt
from armulator.armv6.opcodes.abstract_opcodes.ldrht import Ldrht
from armulator.armv6.opcodes.abstract_opcodes.ldrsbt import Ldrsbt
from armulator.armv6.opcodes.abstract_opcodes.ldrsht import Ldrsht
from armulator.armv6.opcodes.abstract_opcodes.ldrt import Ldrt
from armulator.armv6.opcodes.abstract_opcodes.strbt import Strbt
from armulator.armv6.opcodes.abstract_opcodes.strht import Strht
from armulator.armv6.opcodes.abstract_opcodes.strt import Strt
from armulator.armv6.opcodes.decode_instruction import decode_instruction as op_decode_instruction
from armulator.armv6.permissions import Permissions
from armulator.armv6.registers import Registers
from armulator.armv6.tlb_record import TLBRecord


class ArmV6:
    def __init__(self, config_file=path.join(path.abspath(path.dirname(__file__)), 'arm_configurations.json')):
        configurations.load(config_file)
        self.registers = Registers()
        self.run = True
        self.opcode = 0
        self.opcode_len = 0
        self.mem = MemoryControllerHub.from_memory_list(configurations.memory_list)
        self.is_wait_for_event = False
        self.is_wait_for_interrupt = False
        self.executed_opcode = None

    def start(self):
        self.take_reset()

    def print_registers(self):
        print("{0}:{1}".format("R0", self.registers.get(0)))
        print("{0}:{1}".format("R1", self.registers.get(1)))
        print("{0}:{1}".format("R2", self.registers.get(2)))
        print("{0}:{1}".format("R3", self.registers.get(3)))
        print("{0}:{1}".format("R4", self.registers.get(4)))
        print("{0}:{1}".format("R5", self.registers.get(5)))
        print("{0}:{1}".format("R6", self.registers.get(6)))
        print("{0}:{1}".format("R7", self.registers.get(7)))
        print("{0}:{1}".format("R8", self.registers.get(8)))
        print("{0}:{1}".format("R9", self.registers.get(9)))
        print("{0}:{1}".format("R10", self.registers.get(10)))
        print("{0}:{1}".format("R11", self.registers.get(11)))
        print("{0}:{1}".format("R12", self.registers.get(12)))
        print("{0}:{1}".format("SP", self.registers.get_sp()))
        print("{0}:{1}".format("LR", self.registers.get_lr()))
        print("{0}:{1}".format("PC", self.registers.pc_store_value()))
        print("{0}:{1}".format("CPSR", self.registers.cpsr.value))

    def take_reset(self):
        self.registers.cpsr.m = 0b10011
        if have_security_ext():
            self.registers.scr.ns = 0
        self.registers.reset_control_registers()
        if have_adv_simd_or_vfp():
            self.registers.fpexc.en = 0
        if have_thumbee():
            self.registers.teecr.xed = 0
        if have_jazelle():
            self.registers.jmcr.je = 0
        self.registers.cpsr.i = 1
        self.registers.cpsr.f = 1
        self.registers.cpsr.a = 1
        self.registers.cpsr.it = 0b00000000
        self.registers.cpsr.j = 0
        self.registers.cpsr.t = self.registers.sctlr.te
        self.registers.cpsr.e = self.registers.sctlr.ee
        reset_vector = (
            configurations.impdef_reset_vector if has_imp_def_reset_vector() else self.registers.exc_vector_base()
        )
        reset_vector = set_bit_at(reset_vector, 0, 0)
        self.registers.branch_to(reset_vector)

    def encode_ldfsr(self, dtype: DAbort, level: int) -> int:
        result = 0b000000
        if dtype == DAbort.ACCESS_FLAG:
            result = set_substring(result, 5, 2, 0b0010)
            result = set_substring(result, 1, 0, substring(level, 1, 0))
        elif dtype == DAbort.ALIGNMENT:
            result = 0b100001
        elif dtype == DAbort.PERMISSION:
            result = set_substring(result, 5, 2, 0b0011)
            result = set_substring(result, 1, 0, substring(level, 1, 0))
        elif dtype == DAbort.TRANSLATION:
            result = set_substring(result, 5, 2, 0b0001)
            result = set_substring(result, 1, 0, substring(level, 1, 0))
        elif dtype == DAbort.SYNC_EXTERNAL:
            result = 0b100000
        elif dtype == DAbort.SYNC_EXTERNAL_ON_WALK:
            result = set_substring(result, 5, 2, 0b0101)
            result = set_substring(result, 1, 0, substring(level, 1, 0))
        elif dtype == DAbort.SYNC_PARITY:
            result = 0b011000
        elif dtype == DAbort.SYNC_PARITY_ON_WALK:
            result = set_substring(result, 5, 2, 0b0111)
            result = set_substring(result, 1, 0, substring(level, 1, 0))
        elif dtype == DAbort.ASYNC_PARITY:
            result = 0b011001
        elif dtype == DAbort.ASYNC_EXTERNAL:
            result = 0b010001
        elif dtype == DAbort.SYNC_WATCHPOINT or dtype == DAbort.ASYNC_WATCHPOINT:
            result = 0b100010
        elif dtype == DAbort.TLB_CONFLICT:
            result = 0b110000
        elif dtype == DAbort.LOCKDOWN:
            result = 0b110100
        elif dtype == DAbort.COPROC:
            result = 0b111010
        else:
            pass  # unknown
        return result

    def encode_sdfsr(self, dtype: DAbort, level: int) -> int:
        result = 0b00000
        if dtype == DAbort.ACCESS_FLAG:
            if level == 1:
                result = 0b00011
            else:
                result = 0b00110
        elif dtype == DAbort.ALIGNMENT:
            result = 0b00001
        elif dtype == DAbort.PERMISSION:
            result = set_substring(result, 4, 2, 0b011)
            result = set_bit_at(result, 0, 1)
            result = set_bit_at(result, 1, bit_at(level, 1))
        elif dtype == DAbort.DOMAIN:
            result = set_substring(result, 4, 2, 0b010)
            result = set_bit_at(result, 0, 1)
            result = set_bit_at(result, 1, bit_at(level, 1))
        elif dtype == DAbort.TRANSLATION:
            result = set_substring(result, 4, 2, 0b001)
            result = set_bit_at(result, 0, 1)
            result = set_bit_at(result, 1, bit_at(level, 1))
        elif dtype == DAbort.SYNC_EXTERNAL:
            result = 0b01000
        elif dtype == DAbort.SYNC_EXTERNAL_ON_WALK:
            result = set_substring(result, 4, 2, 0b011)
            result = set_bit_at(result, 0, 0)
            result = set_bit_at(result, 1, bit_at(level, 1))
        elif dtype == DAbort.SYNC_PARITY:
            result = 0b11001
        elif dtype == DAbort.SYNC_PARITY_ON_WALK:
            result = set_substring(result, 4, 2, 0b111)
            result = set_bit_at(result, 0, 0)
            result = set_bit_at(result, 1, bit_at(level, 1))
        elif dtype == DAbort.ASYNC_PARITY:
            result = 0b11000
        elif dtype == DAbort.ASYNC_EXTERNAL:
            result = 0b10110
        elif dtype == DAbort.SYNC_WATCHPOINT or dtype == DAbort.ASYNC_WATCHPOINT:
            result = 0b00010
        elif dtype == DAbort.TLB_CONFLICT:
            result = 0b10000
        elif dtype == DAbort.LOCKDOWN:
            result = 0b10100
        elif dtype == DAbort.COPROC:
            result = 0b11010
        elif dtype == DAbort.ICACHE_MAINT:
            result = 0b00100
        else:
            pass  # unknown
        return result

    def encode_pmsafsr(self, dtype):
        if dtype == DAbort.ALIGNMENT:
            return 0b00001
        elif dtype == DAbort.PERMISSION:
            return 0b01101
        elif dtype == DAbort.SYNC_EXTERNAL:
            return 0b01000
        elif dtype == DAbort.SYNC_PARITY:
            return 0b11001
        elif dtype == DAbort.ASYNC_PARITY:
            return 0b11000
        elif dtype == DAbort.ASYNC_EXTERNAL:
            return 0b10110
        elif dtype == DAbort.SYNC_WATCHPOINT or dtype == DAbort.ASYNC_WATCHPOINT:
            return 0b00010
        elif dtype == DAbort.BACKGROUND:
            return 0b00000
        elif dtype == DAbort.LOCKDOWN:
            return 0b10100
        elif dtype == DAbort.COPROC:
            return 0b11010
        return 0b00000

    def current_cond(self):
        if self.registers.current_instr_set() == InstrSet.ARM:
            return substring(self.opcode, 31, 28)
        if self.opcode_len == 16 and substring(self.opcode, 15, 12) == 0b1101:
            return substring(self.opcode, 11, 8)
        if self.opcode_len == 32 and substring(self.opcode, 31, 27) == 0b11110 and \
                substring(self.opcode, 15, 14) == 0b10 and not bit_at(self.opcode, 12):
            return substring(self.opcode, 25, 22)
        if substring(self.registers.cpsr.it, 3, 0) != 0b0000:
            return substring(self.registers.cpsr.it, 7, 4)
        elif self.registers.cpsr.it == 0b00000000:
            return 0b1110
        print('unpredictable')
        return 0

    def condition_passed(self):
        cond = self.current_cond()
        higher = substring(cond, 3, 1)
        result = 0
        if higher == 0b000:
            result = self.registers.cpsr.z
        elif higher == 0b001:
            result = self.registers.cpsr.c
        elif higher == 0b010:
            result = self.registers.cpsr.n
        elif higher == 0b011:
            result = self.registers.cpsr.v
        elif higher == 0b100:
            result = bool(self.registers.cpsr.c) and not self.registers.cpsr.z
        elif higher == 0b101:
            result = self.registers.cpsr.n == self.registers.cpsr.v
        elif higher == 0b110:
            result = (self.registers.cpsr.n == self.registers.cpsr.v) and not self.registers.cpsr.z
        elif higher == 0b111:
            result = True
        if lower_chunk(cond, 1) and cond != 0b1111:
            result = not result
        return result

    def this_instr_length(self):
        return self.opcode_len

    def this_instr(self):
        return self.opcode

    def write_hsr(self, ec, hsr_string):
        hsr_value = 0x00000000
        hsr_value = set_substring(hsr_value, 31, 26, ec)

        if (ec in (0x0, 0x20, 0x21)) or (ec in (0x24, 0x25) and bit_at(hsr_string, 17)):
            hsr_value = set_bit_at(hsr_value, 25, 1 if self.this_instr_length() == 32 else 0)
        if substring(ec, 5, 4) == 0b00 and substring(ec, 3, 0) != 0b0000:
            if self.registers.current_instr_set() == InstrSet.ARM:
                hsr_value = set_bit_at(hsr_value, 24, 1)
                hsr_value = set_substring(hsr_value, 23, 20, self.current_cond())
            else:
                hsr_value = set_bit_at(hsr_value, 24, configurations.write_hsr_hsr_value_24)
                if bit_at(hsr_value, 24):
                    if self.condition_passed():
                        cond = self.current_cond() if configurations.write_hsr_23_22_cond else 0b1110
                    else:
                        cond = self.current_cond()
                    hsr_value = set_substring(hsr_value, 23, 20, cond)
            hsr_value = set_substring(hsr_value, 19, 0, substring(hsr_string, 19, 0))
        else:
            hsr_value = set_substring(hsr_value, 24, 0, hsr_string)
        self.registers.hsr.value = hsr_value

    def switch_to_jazelle_execution(self):
        raise NotImplementedError()

    def branch_write_pc(self, address):
        if self.registers.current_instr_set() == InstrSet.ARM:
            if arch_version() < 6 and lower_chunk(address, 2) != 0b00:
                print('unpredictable')
            self.registers.branch_to(set_substring(address, 1, 0, 0))
        elif self.registers.current_instr_set() == InstrSet.JAZELLE:
            if jazelle_accepts_execution():
                self.registers.branch_to(address)
            else:
                self.registers.branch_to(set_substring(address, 1, 0, 0))
        else:
            self.registers.branch_to(set_bit_at(address, 0, 0))

    def bx_write_pc(self, address):
        if self.registers.current_instr_set() == InstrSet.THUMB_EE:
            if bit_at(address, 0):
                address = set_bit_at(address, 0, 0)
                self.registers.branch_to(address)
            else:
                print('unpredictable')
        else:
            if bit_at(address, 0):
                self.registers.select_instr_set(InstrSet.THUMB)
                address = set_bit_at(address, 0, 0)
                self.registers.branch_to(address)
            elif not bit_at(address, 1):
                self.registers.select_instr_set(InstrSet.ARM)
                self.registers.branch_to(address)
            else:
                print('unpredictable')

    def alu_write_pc(self, address):
        if arch_version() >= 7 and self.registers.current_instr_set() == InstrSet.ARM:
            self.bx_write_pc(address)
        else:
            self.branch_write_pc(address)

    def load_write_pc(self, address):
        if arch_version() >= 5:
            self.bx_write_pc(address)
        else:
            self.branch_write_pc(address)

    def tlb_lookup_came_from_cache_maintenance(self):
        # mock
        raise NotImplementedError()

    def ls_instruction_syndrome(self):
        if not hasattr(self.executed_opcode, "instruction_syndrome"):
            return 0b000000000
        elif (isinstance(self.executed_opcode, (Strt, Strht, Strbt, Ldrt, Ldrht, Ldrsht, Ldrbt, Ldrsbt)) and
              self.registers.current_instr_set() == InstrSet.ARM):
            return 0b000000000
        else:
            return self.executed_opcode.instruction_syndrome()

    def null_check_if_thumbee(self, n: int):
        if self.registers.current_instr_set() == InstrSet.THUMB_EE:
            if n == 15:
                if align(self.registers.get_pc(), 4) == 0:
                    print('unpredictable')
            elif n == 13:
                if self.registers.get_sp() == 0:
                    print('unpredictable')
            else:
                if self.registers.get(n) == 0:
                    self.registers.set_lr(self.registers.get_pc() | 0b1)
                    self.registers.cpsr.it = 0b00000000
                    self.branch_write_pc(self.registers.teehbr - 4)
                    raise EndOfInstruction("NullCheckIfThumbEE")

    def fcse_translate(self, va):
        if substring(va, 31, 25) == 0b0000000:
            mva = chain(self.registers.fcseidr.pid, substring(va, 24, 0), 25)
        else:
            mva = va
        return mva

    def default_memory_attributes(self, va):
        memattrs = MemoryAttributes()
        if substring(va, 39, 38) == 0b00:
            if not self.registers.sctlr.c:
                memattrs.type = MemType.NORMAL
                memattrs.innerattrs = 0b00
                memattrs.shareable = True
            else:
                memattrs.type = MemType.NORMAL
                memattrs.innerattrs = 0b01
                memattrs.shareable = False
        elif substring(va, 39, 38) == 0b01:
            if not self.registers.sctlr.c or bit_at(va, 37):
                memattrs.type = MemType.NORMAL
                memattrs.innerattrs = 0b00
                memattrs.shareable = True
            else:
                memattrs.type = MemType.NORMAL
                memattrs.innerattrs = 0b10
                memattrs.shareable = False
        elif substring(va, 39, 38) == 0b10:
            memattrs.type = MemType.DEVICE
            memattrs.innerattrs = 0b00
            memattrs.shareable = bit_at(va, 37)
        elif substring(va, 39, 38) == 0b11:
            memattrs.type = MemType.STRONGLY_ORDERED
            memattrs.innerattrs = 0b00
            memattrs.shareable = True
        memattrs.outerattrs = memattrs.innerattrs
        memattrs.outershareable = memattrs.shareable
        return memattrs

    def convert_attrs_hints(self, rgn: int) -> int:
        if rgn == 0b00:
            attributes = 0b00
            hints = 0b00
        elif bit_at(rgn, 0) == 0b1:
            attributes = 0b11
            hints = chain(1, int(not bit_at(rgn, 1)), 1)
        else:
            attributes = 0b10
            hints = 0b10
        return chain(hints, attributes, 2)

    def check_permission(self, perms, mva, level, domain, iswrite, ispriv, taketohypmode, ldfsr_format):
        secondstageabort = False
        ipavalid = False
        s2fs1walk = False
        ipa = 0b0000000000000000000000000000000000000000
        if self.registers.sctlr.afe:
            perms.ap = set_bit_at(perms.ap, 0, 1)
        abort = False
        if perms.ap == 0b000:
            abort = True
        elif perms.ap == 0b001:
            abort = not ispriv
        elif perms.ap == 0b010:
            abort = not ispriv and iswrite
        elif perms.ap == 0b011:
            abort = False
        elif perms.ap == 0b100:
            print('unpredictable')
        elif perms.ap == 0b101:
            abort = not ispriv or iswrite
        elif perms.ap == 0b110:
            abort = iswrite
        elif perms.ap == 0b111:
            if memory_system_architecture() == MemArch.VMSA:
                abort = iswrite
            else:
                print('unpredictable')
        if abort:
            self.data_abort(mva, ipa, domain, level, iswrite, DAbort.PERMISSION, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)

    def check_permission_s2(self, perms: Permissions, mva, ipa, level, iswrite, s2fs1walk):
        abort = (iswrite and bit_at(perms.ap, 2) == 0) or (not iswrite and bit_at(perms.ap, 1) == 0)
        if abort:
            domain = 0b0000  # unknown
            taketohypmode = True
            secondstageabort = True
            ipavalid = s2fs1walk
            ldfsr_format = True
            self.data_abort(mva, ipa, domain, level, iswrite, DAbort.PERMISSION, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)

    def check_domain(self, domain: int, mva: int, level: int, iswrite: bool) -> bool:
        ipaddress = 0b0000000000000000000000000000000000000000  # unknown
        taketohypmode = False
        secondstageabort = False
        ipavalid = False
        ldfsr_format = False
        s2fs1walk = False
        permission_check = False
        domain_acess_permission = self.registers.dacr.get_d_n(domain)
        if domain_acess_permission == 0b00:
            self.data_abort(mva, ipaddress, domain, level, iswrite, DAbort.DOMAIN, taketohypmode,
                            secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
        elif domain_acess_permission == 0b01:
            permission_check = True
        elif domain_acess_permission == 0b10:
            print('unpredictable')
        elif domain_acess_permission == 0b11:
            permission_check = False
        return permission_check

    def second_stage_translate(self, s1_out_addr_desc, mva, size, is_write):
        result = AddressDescriptor()
        if have_virt_ext() and not self.registers.is_secure() and not self.registers.current_mode_is_hyp():
            if self.registers.hcr.vm:
                s2ia = s1_out_addr_desc.paddress.physicaladdress
                stage1 = False
                s2fs1walk = True
                tlbrecord_s2 = self.translation_table_walk_ld(s2ia, mva, is_write, stage1, s2fs1walk, size)
                self.check_permission_s2(tlbrecord_s2.perms, mva, s2ia, tlbrecord_s2.level, False, s2fs1walk)
                if self.registers.hcr.ptw:
                    if tlbrecord_s2.addrdesc.memattrs.type != MemType.NORMAL:
                        domain = 0b0000  # unknown
                        taketohypmode = True
                        secondstageabort = True
                        ipavalid = True
                        ldfsr_format = True
                        s2fs1walk = True
                        self.data_abort(mva, s2ia, domain, tlbrecord_s2.level, is_write, DAbort.PERMISSION,
                                        taketohypmode, secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
                result = self.combine_s1s2_desc(s1_out_addr_desc, tlbrecord_s2.addrdesc)
            else:
                result = s1_out_addr_desc
        return result

    def data_abort(self, vaddress, ipaddress, domain, level, iswrite, dtype, taketohypmode, secondstageabort, ipavalid,
                   ldfsr_format, s2fs1walk):
        if memory_system_architecture() == MemArch.VMSA:
            if not taketohypmode:
                dfsr_string = 0b00000000000000
                if (dtype in (DAbort.ASYNC_PARITY, DAbort.ASYNC_EXTERNAL, DAbort.ASYNC_WATCHPOINT) or
                        (dtype == DAbort.SYNC_WATCHPOINT and self.registers.dbgdidr.version <= 4)):
                    self.registers.dfar = 0x00000000  # unknown
                else:
                    self.registers.dfar = vaddress
                if ldfsr_format:
                    dfsr_string = set_bit_at(dfsr_string, 13, int(self.tlb_lookup_came_from_cache_maintenance()))
                    if dtype in (DAbort.ASYNC_EXTERNAL, DAbort.SYNC_EXTERNAL):
                        dfsr_string = set_bit_at(dfsr_string, 12, configurations.dfsr_string_12)
                    else:
                        dfsr_string = set_bit_at(dfsr_string, 12, 0)
                    if dtype in (DAbort.SYNC_WATCHPOINT, DAbort.ASYNC_WATCHPOINT):
                        dfsr_string = set_bit_at(dfsr_string, 11, 0)  # unknown
                    else:
                        dfsr_string = set_bit_at(dfsr_string, 11, 1 if iswrite else 0)
                    dfsr_string = set_bit_at(dfsr_string, 10, 0)  # unknown
                    dfsr_string = set_bit_at(dfsr_string, 9, 1)
                    dfsr_string = set_substring(dfsr_string, 8, 6, 0b000)  # unknown
                    dfsr_string = set_substring(dfsr_string, 5, 0, self.encode_ldfsr(dtype, level))
                else:
                    if have_lpae():
                        dfsr_string = set_bit_at(dfsr_string, 13, int(self.tlb_lookup_came_from_cache_maintenance()))
                    if dtype in (DAbort.ASYNC_EXTERNAL, DAbort.SYNC_EXTERNAL):
                        dfsr_string = set_bit_at(dfsr_string, 12, configurations.dfsr_string_12)
                    else:
                        dfsr_string = set_bit_at(dfsr_string, 12, 0)
                    if dtype in (DAbort.SYNC_WATCHPOINT, DAbort.ASYNC_WATCHPOINT):
                        dfsr_string = set_bit_at(dfsr_string, 11, 0)  # unknown
                    else:
                        dfsr_string = set_bit_at(dfsr_string, 11, 1 if iswrite else 0)
                    dfsr_string = set_bit_at(dfsr_string, 9, 0)
                    dfsr_string = set_bit_at(dfsr_string, 8, 0)  # unknown
                    domain_valid = (
                            dtype == DAbort.DOMAIN or
                            (
                                    level == 2 and
                                    dtype in (
                                        DAbort.TRANSLATION,
                                        DAbort.ACCESS_FLAG,
                                        DAbort.SYNC_EXTERNAL_ON_WALK,
                                        DAbort.SYNC_PARITY_ON_WALK
                                    )
                            ) or (not have_lpae() and dtype == DAbort.PERMISSION))
                    if domain_valid:
                        dfsr_string = set_substring(dfsr_string, 7, 4, domain)
                    else:
                        dfsr_string = set_substring(dfsr_string, 7, 4, 0b0000)  # unknown
                    temp_sdfsr = self.encode_sdfsr(dtype, level)
                    dfsr_string = set_bit_at(dfsr_string, 10, bit_at(temp_sdfsr, 4))
                    dfsr_string = set_substring(dfsr_string, 3, 0, substring(temp_sdfsr, 3, 0))
                self.registers.dfsr.value = set_substring(self.registers.dfsr.value, 13, 0, dfsr_string)
            else:
                hsr_string = 0b0000000000000000000000000
                self.registers.hdfar = vaddress
                if ipavalid:
                    self.registers.hpfar.fipa = substring(ipaddress, 39, 12)
                if secondstageabort:
                    ec = 0b100100
                    hsr_string = set_substring(hsr_string, 24, 16, self.ls_instruction_syndrome())
                else:
                    ec = 0b100101
                    hsr_string = set_bit_at(hsr_string, 24, 0)
                if dtype in (DAbort.ASYNC_EXTERNAL, DAbort.SYNC_EXTERNAL):
                    hsr_string = set_bit_at(hsr_string, 9, configurations.data_abort_hsr_9)
                else:
                    hsr_string = set_bit_at(hsr_string, 9, 0)
                hsr_string = set_bit_at(hsr_string, 8, 1 if self.tlb_lookup_came_from_cache_maintenance() else 0)
                hsr_string = set_bit_at(hsr_string, 7, 1 if s2fs1walk else 0)
                hsr_string = set_bit_at(hsr_string, 6, 1 if iswrite else 0)
                hsr_string = set_substring(hsr_string, 5, 0, self.encode_ldfsr(dtype, level))
                self.write_hsr(ec, hsr_string)
        else:
            dfsr_string = 0b00000000000000
            if (dtype in (DAbort.ASYNC_PARITY, DAbort.ASYNC_EXTERNAL, DAbort.ASYNC_WATCHPOINT) or
                    (dtype == DAbort.SYNC_WATCHPOINT and self.registers.dbgdidr.version <= 4)):
                self.registers.dfar = 0x00000000  # unknown
            elif dtype == DAbort.SYNC_PARITY:
                if configurations.data_abort_pmsa_change_dfar:
                    self.registers.dfar = vaddress
            else:
                self.registers.dfar = vaddress
            if dtype in (DAbort.ASYNC_EXTERNAL, DAbort.SYNC_EXTERNAL):
                dfsr_string = set_bit_at(dfsr_string, 12, configurations.dfsr_string_12)
            else:
                dfsr_string = set_bit_at(dfsr_string, 12, 0)
            if dtype in (DAbort.SYNC_WATCHPOINT, DAbort.ASYNC_WATCHPOINT):
                dfsr_string = set_bit_at(dfsr_string, 11, 0)  # unknown
            else:
                dfsr_string = set_bit_at(dfsr_string, 11, iswrite)
            temp_pmsafsr = self.encode_pmsafsr(dtype)
            dfsr_string = set_bit_at(dfsr_string, 10, bit_at(temp_pmsafsr, 4))
            dfsr_string = set_substring(dfsr_string, 3, 0, substring(temp_pmsafsr, 3, 0))
            self.registers.dfsr.value = set_substring(self.registers.dfsr.value, 13, 0, dfsr_string)
        raise DataAbortException(dtype, secondstageabort)

    def alignment_fault_v(self, address, iswrite, taketohyp, secondstageabort):
        ipaddress = 0b0000000000000000000000000000000000000000  # unknown
        domain = 0b0000  # unknown
        level = 0  # unknown
        ipavalid = False
        ldfsr_fromat = taketohyp or self.registers.ttbcr.eae
        s2fs1walk = False
        mva = self.fcse_translate(address)
        self.data_abort(mva, ipaddress, domain, level, iswrite, DAbort.ALIGNMENT, taketohyp,
                        secondstageabort, ipavalid, ldfsr_fromat, s2fs1walk)

    def alignment_fault_p(self, address, iswrite):
        ipaddress = 0b0000000000000000000000000000000000000000  # unknown
        domain = 0b0000  # unknown
        level = 0  # unknown
        taketohypmode = False
        secondstageabort = False
        ipavalid = False
        ldfsr_fromat = False
        s2fs1walk = False
        self.data_abort(address, ipaddress, domain, level, iswrite, DAbort.ALIGNMENT, taketohypmode,
                        secondstageabort, ipavalid, ldfsr_fromat, s2fs1walk)

    def alignment_fault(self, address, iswrite):
        if memory_system_architecture() == MemArch.VMSA:
            taketohypmode = self.registers.current_mode_is_hyp() or self.registers.hcr.tge
            secondstageabort = False
            self.alignment_fault_v(address, iswrite, taketohypmode, secondstageabort)
        elif memory_system_architecture() == MemArch.PMSA:
            self.alignment_fault_p(address, iswrite)

    def combine_s1s2_desc(self, s1desc: AddressDescriptor, s2desc: AddressDescriptor) -> AddressDescriptor:
        result = AddressDescriptor()
        result.paddress = s2desc.paddress
        result.memattrs.innerattrs = 0b00  # unknown
        result.memattrs.outerattrs = 0b00  # unknown
        result.memattrs.innerhints = 0b00  # unknown
        result.memattrs.outerhints = 0b00  # unknown
        result.memattrs.shareable = True
        result.memattrs.outershareable = True
        if s2desc.memattrs.type == MemType.STRONGLY_ORDERED or s1desc.memattrs.type == MemType.STRONGLY_ORDERED:
            result.memattrs.type = MemType.STRONGLY_ORDERED
        elif s2desc.memattrs.type == MemType.DEVICE or s1desc.memattrs.type == MemType.DEVICE:
            result.memattrs.type = MemType.DEVICE
        else:
            result.memattrs.type = MemType.NORMAL
        if result.memattrs.type == MemType.NORMAL:
            if s2desc.memattrs.innerattrs == 0b01 or s1desc.memattrs.innerattrs == 0b01:
                result.memattrs.innerattrs = 0b00  # unknown
            elif s2desc.memattrs.innerattrs == 0b00 or s1desc.memattrs.innerattrs == 0b00:
                #  either encoding Non-cacheable
                result.memattrs.innerattrs = 0b00
            elif s2desc.memattrs.innerattrs == 0b10 or s1desc.memattrs.innerattrs == 0b10:
                # either encoding Write-Through cacheable
                result.memattrs.innerattrs = 0b10
            else:
                # both encodings Write-Back
                result.memattrs.innerattrs = 0b11
            if s2desc.memattrs.outerattrs == 0b01 or s1desc.memattrs.outerattrs == 0b01:
                result.memattrs.outerattrs = 0b00  # unknown
            elif s2desc.memattrs.outerattrs == 0b00 or s1desc.memattrs.outerattrs == 0b00:
                result.memattrs.outerattrs = 0b00
            elif s2desc.memattrs.outerattrs == 0b10 or s1desc.memattrs.outerattrs == 0b10:
                result.memattrs.outerattrs = 0b10
            else:
                result.memattrs.outerattrs = 0b11
            result.memattrs.innerhints = s1desc.memattrs.innerhints
            result.memattrs.outerhints = s1desc.memattrs.outerhints
            result.memattrs.shareable = s1desc.memattrs.shareable or s2desc.memattrs.shareable
            result.memattrs.outershareable = s1desc.memattrs.outershareable or s2desc.memattrs.outershareable
            # another check for normal memtype according to the documentation
            if result.memattrs.innerattrs == 0b00 and result.memattrs.outerattrs == 0b00:
                result.memattrs.shareable = True
                result.memattrs.outershareable = True
        return result

    def mair_decode(self, attr):
        memattrs = MemoryAttributes()
        if self.registers.current_mode_is_hyp():
            mair = chain(self.registers.hmair1, self.registers.hmair0, 32)
        else:
            mair = chain(self.registers.mair1, self.registers.mair0, 32)
        index = attr
        attrfield = substring(mair, 8 * index + 7, 8 * index)
        if substring(attrfield, 7, 4) == 0b0000:
            unpackinner = False
            memattrs.innerattrs = 0b00  # unknown
            memattrs.outerattrs = 0b00  # unknown
            memattrs.innerhints = 0b00  # unknown
            memattrs.outerhints = 0b00  # unknown
            memattrs.innertransient = False  # unknown
            memattrs.outertransient = False  # unknown
            if substring(attrfield, 3, 0) == 0b0000:
                memattrs.type = MemType.STRONGLY_ORDERED
            elif substring(attrfield, 3, 0) == 0b0100:
                memattrs.type = MemType.DEVICE
            else:
                # implementation defined
                pass
        elif substring(attrfield, 7, 6) == 0b00:
            unpackinner = True
            if implementation_supports_transient():
                memattrs.type = MemType.NORMAL
                memattrs.outerhints = substring(attrfield, 5, 4)
                memattrs.outerattrs = 0b10
                memattrs.outertransient = True
            else:
                # implementation defined
                pass
        elif substring(attrfield, 7, 6) == 0b01:
            unpackinner = True
            if substring(attrfield, 5, 4) == 0b00:
                memattrs.type = MemType.NORMAL
                memattrs.outerhints = 0b00
                memattrs.outerattrs = 0b00
                memattrs.outertransient = False
            else:
                if implementation_supports_transient():
                    memattrs.type = MemType.NORMAL
                    memattrs.outerhints = substring(attrfield, 5, 4)
                    memattrs.outerattrs = 0b11
                    memattrs.outertransient = True
                else:
                    # implementation defined
                    pass
        else:
            unpackinner = True
            memattrs.type = MemType.NORMAL
            memattrs.outerhints = substring(attrfield, 5, 4)
            memattrs.outerattrs = substring(attrfield, 7, 6)
            memattrs.outertransient = False
        if unpackinner:
            if bit_at(attrfield, 3) == 1:
                memattrs.innerhints = substring(attrfield, 1, 0)
                memattrs.innerattrs = substring(attrfield, 3, 2)
                memattrs.innertransient = False
            elif substring(attrfield, 2, 0) == 0b100:
                memattrs.innerhints = 0b00
                memattrs.innerattrs = 0b00
                memattrs.innertransient = True
            else:
                if implementation_supports_transient():
                    if bit_at(attrfield, 2) == 0:
                        memattrs.innerhints = substring(attrfield, 1, 0)
                        memattrs.innerattrs = 0b10
                        memattrs.innertransient = True
                    else:
                        memattrs.innerhints = substring(attrfield, 1, 0)
                        memattrs.innerattrs = 0b11
                        memattrs.innertransient = True
                else:
                    # implementation defined
                    pass
        return memattrs

    def s2_attr_decode(self, attr: int):
        memattrs = MemoryAttributes()
        if substring(attr, 3, 2) == 0b00:
            memattrs.innerattrs = 0b00  # unknown
            memattrs.outerattrs = 0b00  # unknown
            memattrs.innerhints = 0b00  # unknown
            memattrs.outerhints = 0b00  # unknown
            if substring(attr, 1, 0) == 0b00:
                memattrs.type = MemType.STRONGLY_ORDERED
            elif substring(attr, 1, 0) == 0b01:
                memattrs.type = MemType.DEVICE
            else:
                memattrs.type = MemType.NORMAL  # unknown
        else:
            memattrs.type = MemType.NORMAL
            if bit_at(attr, 3) == 0:
                memattrs.outerattrs = 0b00
                memattrs.outerhints = 0b00
            else:
                memattrs.outerattrs = substring(attr, 3, 2)
                memattrs.outerhints = 0b11
            if substring(attr, 1, 0) == 0b00:
                memattrs.type = MemType.NORMAL  # unknown
                memattrs.innerattrs = 0b00  # unknown
                memattrs.outerattrs = 0b00  # unknown
                memattrs.innerhints = 0b00  # unknown
                memattrs.outerhints = 0b00  # unknown
            elif bit_at(attr, 1) == 0:
                memattrs.innerattrs = 0b00
                memattrs.innerhints = 0b00
            else:
                memattrs.innerattrs = 0b11
                memattrs.innerhints = substring(attr, 1, 0)
        return memattrs

    def remap_regs_have_reset_values(self):
        # mock
        raise NotImplementedError()

    def default_tex_decode(self, texcb, s):
        memattrs = MemoryAttributes()
        if texcb == 0b00000:
            memattrs.type = MemType.STRONGLY_ORDERED
            memattrs.innerattrs = 0b00  # unknown
            memattrs.innerhints = 0b00  # unknown
            memattrs.outerattrs = 0b00  # unknown
            memattrs.outerhints = 0b00  # unknown
            memattrs.shareable = True
        elif texcb == 0b00001:
            memattrs.type = MemType.DEVICE
            memattrs.innerattrs = 0b00  # unknown
            memattrs.innerhints = 0b00  # unknown
            memattrs.outerattrs = 0b00  # unknown
            memattrs.outerhints = 0b00  # unknown
            memattrs.shareable = True
        elif texcb == 0b00010:
            memattrs.type = MemType.NORMAL
            memattrs.innerattrs = 0b10
            memattrs.innerhints = 0b10
            memattrs.outerattrs = 0b10
            memattrs.outerhints = 0b10
            memattrs.shareable = s == 1
        elif texcb == 0b00011:
            memattrs.type = MemType.NORMAL
            memattrs.innerattrs = 0b11
            memattrs.innerhints = 0b10
            memattrs.outerattrs = 0b11
            memattrs.outerhints = 0b10
            memattrs.shareable = s == 1
        elif texcb == 0b00100:
            memattrs.type = MemType.NORMAL
            memattrs.innerattrs = 0b00
            memattrs.innerhints = 0b00
            memattrs.outerattrs = 0b00
            memattrs.outerhints = 0b00
            memattrs.shareable = s == 1
        elif texcb == 0b00110:
            # implementation defined
            pass
        elif texcb == 0b00111:
            memattrs.type = MemType.NORMAL
            memattrs.innerattrs = 0b11
            memattrs.innerhints = 0b11
            memattrs.outerattrs = 0b11
            memattrs.outerhints = 0b11
            memattrs.shareable = s == 1
        elif texcb == 0b01000:
            memattrs.type = MemType.DEVICE
            memattrs.innerattrs = 0b00  # unknown
            memattrs.innerhints = 0b00  # unknown
            memattrs.outerattrs = 0b00  # unknown
            memattrs.outerhints = 0b00  # unknown
            memattrs.shareable = True
        elif bit_at(texcb, 4):
            memattrs.type = MemType.NORMAL
            hintsattrs = self.convert_attrs_hints(substring(texcb, 1, 0))
            memattrs.innerattrs = substring(hintsattrs, 1, 0)
            memattrs.innerhints = substring(hintsattrs, 3, 2)
            hintsattrs = self.convert_attrs_hints(substring(texcb, 3, 2))
            memattrs.outerattrs = substring(hintsattrs, 1, 0)
            memattrs.outerhints = substring(hintsattrs, 3, 2)
            memattrs.shareable = s
        else:
            print('unpredictable')
        memattrs.outershareable = memattrs.shareable
        return memattrs

    def remapped_tex_decode(self, texcb, s):
        memattrs = MemoryAttributes()
        region = substring(texcb, 2, 0)
        if region == 6:
            # IMPLEMENTATION_DEFINED setting of memattrs
            pass
        else:
            if self.registers.prrr.get_tr_n(region) == 0b00:
                memattrs.type = MemType.STRONGLY_ORDERED
                memattrs.innerattrs = 0b00  # unknown
                memattrs.innerhints = 0b00  # unknown
                memattrs.outerattrs = 0b00  # unknown
                memattrs.outerhints = 0b00  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.registers.prrr.get_tr_n(region) == 0b01:
                memattrs.type = MemType.DEVICE
                memattrs.innerattrs = 0b00  # unknown
                memattrs.outerattrs = 0b00  # unknown
                memattrs.innerhints = 0b00  # unknown
                memattrs.outerhints = 0b00  # unknown
                memattrs.shareable = True
                memattrs.outershareable = True
            elif self.registers.prrr.get_tr_n(region) == 0b10:
                memattrs.type = MemType.NORMAL
                hintsattrs = self.convert_attrs_hints(self.registers.nmrr.get_ir_n(region))
                memattrs.innerattrs = substring(hintsattrs, 1, 0)
                memattrs.innerhints = substring(hintsattrs, 3, 2)
                hintsattrs = self.convert_attrs_hints(self.registers.nmrr.get_or_n(region))
                memattrs.outerattrs = substring(hintsattrs, 1, 0)
                memattrs.outerhints = substring(hintsattrs, 3, 2)
                s_bit = self.registers.prrr.ns0 if not s else self.registers.prrr.ns1
                memattrs.shareable = s_bit == 0b1
                memattrs.outershareable = s_bit and not self.registers.prrr.get_nos_n(region)
            elif self.registers.prrr.get_tr_n(region) == 0b11:
                memattrs.type = MemType.NORMAL  # unknown
                memattrs.innerattrs = 0b00  # unknown
                memattrs.innerhints = 0b00  # unknown
                memattrs.outerattrs = 0b00  # unknown
                memattrs.outerhints = 0b00  # unknown
                memattrs.shareable = False  # unknown
                memattrs.outershareable = False  # unknown
        return memattrs

    def translation_table_walk_ld(self, ia: int, va: int, is_write: bool, stage1: bool, s2fs1walk: bool, size: int):
        result = TLBRecord()
        walkaddr = AddressDescriptor()
        domain = 0b0000  # unknown
        ldfsr_format = True
        base_address = 0b0000000000000000000000000000000000000000
        base_found = False
        disabled = False
        if stage1:
            if self.registers.current_mode_is_hyp():
                lookup_secure = False
                t0_size = self.registers.htcr.t0sz
                if t0_size == 0 or substring(ia, 31, 32 - t0_size) == 0:
                    current_level = 1 if substring(self.registers.htcr.t0sz, 2, 1) == 0b00 else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = substring(self.registers.httbr, 39, ba_lower_bound) << ba_lower_bound
                    if substring(self.registers.httbr, ba_lower_bound - 1, 3) != 0:
                        print('unpredictable')
                    base_found = True
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.NORMAL
                    hintsattrs = self.convert_attrs_hints(self.registers.htcr.irgn0)
                    walkaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
                    hintsattrs = self.convert_attrs_hints(self.registers.htcr.rgn0)
                    walkaddr.memattrs.outerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.outerattrs = substring(hintsattrs, 1, 0)
                    walkaddr.memattrs.shareable = bit_at(self.registers.htcr.sh0, 1) == 0b1
                    walkaddr.memattrs.outershareable = self.registers.htcr.sh0 == 0b10
                    walkaddr.paddress.ns = 1
            else:
                lookup_secure = self.registers.is_secure()
                t0_size = self.registers.ttbcr.t0sz
                if t0_size == 0 or substring(ia, 31, 32 - t0_size) == 0:
                    current_level = 1 if substring(self.registers.ttbcr.t0sz, 2, 1) == 0b00 else 2
                    ba_lower_bound = 9 * current_level - t0_size - 4
                    base_address = substring(self.registers.ttbr0_64, 39, ba_lower_bound) << ba_lower_bound
                    if substring(self.registers.ttbr0_64, ba_lower_bound - 1, 3) != 0:
                        print('unpredictable')
                    base_found = True
                    disabled = self.registers.ttbcr.epd0
                    start_bit = 31 - t0_size
                    walkaddr.memattrs.type = MemType.NORMAL
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.irgn0)
                    walkaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.orgn0)
                    walkaddr.memattrs.outerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.outerattrs = substring(hintsattrs, 1, 0)
                    walkaddr.memattrs.shareable = bit_at(self.registers.ttbcr.sh0, 1)
                    walkaddr.memattrs.outershareable = self.registers.ttbcr.sh0 == 0b10
                t1_size = self.registers.ttbcr.t1sz
                if (t1_size == 0 and not base_found) or is_ones(substring(ia, 31, 32 - t1_size), t1_size):
                    current_level = 1 if substring(self.registers.ttbcr.t1sz, 2, 1) == 0b00 else 2
                    ba_lower_bound = 9 * current_level - t1_size - 4
                    base_address = substring(self.registers.ttbr1_64, 39, ba_lower_bound) << ba_lower_bound
                    if substring(self.registers.ttbr1_64, ba_lower_bound - 1, 3) != 0:
                        print('unpredictable')
                    base_found = True
                    disabled = self.registers.ttbcr.epd1
                    start_bit = 31 - t1_size
                    walkaddr.memattrs.type = MemType.NORMAL
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.irgn1)
                    walkaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
                    hintsattrs = self.convert_attrs_hints(self.registers.ttbcr.orgn1)
                    walkaddr.memattrs.outerhints = substring(hintsattrs, 3, 2)
                    walkaddr.memattrs.outerattrs = substring(hintsattrs, 1, 0)
                    walkaddr.memattrs.shareable = bit_at(self.registers.ttbcr.sh1, 1) == 0b1
                    walkaddr.memattrs.outershareable = self.registers.ttbcr.sh1 == 0b10
        else:
            t0_size = to_signed(self.registers.vtcr.t0sz, 4)
            s_level = self.registers.vtcr.sl0
            ba_lower_bound = 14 - t0_size - (9 * s_level)
            if s_level == 0 and t0_size < -2:
                print('unpredictable')
            if s_level == 1 and t0_size > 1:
                print('unpredictable')
            if bit_at(self.registers.vtcr.sl0, 1) == 0b1:
                print('unpredictable')
            if substring(self.registers.vttbr, ba_lower_bound - 1, 3) != 0:
                print('unpredictable')
            if t0_size == -8 or substring(ia, 39, 32 - t0_size) == 0:
                current_level = 2 - s_level
                base_address = substring(self.registers.vttbr, 39, ba_lower_bound) << ba_lower_bound
                base_found = True
                start_bit = 31 - t0_size
            lookup_secure = False
            walkaddr.memattrs.type = MemType.NORMAL
            hintsattrs = self.convert_attrs_hints(self.registers.vtcr.irgn0)
            walkaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
            walkaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
            hintsattrs = self.convert_attrs_hints(self.registers.vtcr.orgn0)
            walkaddr.memattrs.outerhints = substring(hintsattrs, 3, 2)
            walkaddr.memattrs.outerattrs = substring(hintsattrs, 1, 0)
            walkaddr.memattrs.shareable = bit_at(self.registers.vtcr.sh0, 1) == 0b1
            walkaddr.memattrs.outershareable = self.registers.vtcr.sh0 == 0b10
        if not base_found or disabled:
            taketohypmode = self.registers.current_mode_is_hyp() or not stage1
            level = 1
            ipavalid = not stage1
            self.data_abort(va, ia, domain, level, is_write, DAbort.TRANSLATION, taketohypmode, not stage1,
                            ipavalid, ldfsr_format, s2fs1walk)
        first_iteration = True
        table_rw = True
        table_user = True
        table_xn = False
        table_pxn = False
        lookup_finished = True
        output_address = 0b0000000000000000000000000000000000000000
        attrs = 0b0000000000000
        while lookup_finished:
            lookup_finished = True
            block_translate = False
            offset = 9 * current_level
            if first_iteration:
                ia_select = substring(ia, start_bit, 39 - offset) << 3
            else:
                ia_select = substring(ia, 47 - offset, 39 - offset) << 3
            lookup_address = base_address | ia_select
            first_iteration = False
            walkaddr.paddress.physicaladdress = lookup_address
            if lookup_secure:
                walkaddr.paddress.ns = 0
            else:
                walkaddr.paddress.ns = 1
            if not have_virt_ext() or not stage1 or self.registers.is_secure() or self.registers.current_mode_is_hyp():
                if have_virt_ext() and (self.registers.current_mode_is_hyp() or not stage1):
                    big_endian = self.registers.hsctlr.ee
                else:
                    big_endian = self.registers.sctlr.ee
                descriptor = self.mem[walkaddr, 8]
                if big_endian:
                    descriptor = big_endian_reverse(descriptor, 8)
            else:
                walkaddr2 = self.second_stage_translate(walkaddr, substring(ia, 31, 0), 8, is_write)
                descriptor = self.mem[walkaddr2, 8]
                if self.registers.sctlr.ee:
                    descriptor = big_endian_reverse(descriptor, 8)
            if bit_at(descriptor, 0) == 0:
                taketohypmode = self.registers.current_mode_is_hyp() or not stage1
                ipavalid = not stage1
                self.data_abort(va, ia, domain, current_level, is_write, DAbort.TRANSLATION, taketohypmode,
                                not stage1, ipavalid, ldfsr_format, s2fs1walk)
            else:
                if bit_at(descriptor, 1) == 0:
                    if current_level == 3:
                        taketohypmode = self.registers.current_mode_is_hyp() or not stage1
                        ipavalid = not stage1
                        self.data_abort(va, ia, domain, current_level, is_write, DAbort.TRANSLATION,
                                        taketohypmode, not stage1, ipavalid, ldfsr_format, s2fs1walk)
                    else:
                        block_translate = True
                else:
                    if current_level == 3:
                        block_translate = True
                    else:
                        base_address = substring(descriptor, 39, 12) << 12
                        lookup_secure = lookup_secure and bit_at(descriptor, 63) == 0
                        table_rw = table_rw and bit_at(descriptor, 62) == 0
                        table_user = table_user and bit_at(descriptor, 61) == 0
                        table_pxn = table_pxn or bit_at(descriptor, 59) == 1
                        table_xn = table_xn or bit_at(descriptor, 60) == 1
                        lookup_finished = False
            if block_translate:
                ia_length = 39 - offset
                output_address = chain(substring(descriptor, 39, ia_length), substring(ia, ia_length - 1, 0), ia_length)
                attrs = chain(substring(descriptor, 54, 52), substring(descriptor, 11, 2), 10)
                if stage1:
                    if table_xn:
                        attrs = set_bit_at(attrs, 12, 1)
                    if table_pxn:
                        attrs = set_bit_at(attrs, 11, 1)
                    if self.registers.is_secure() and not lookup_secure:
                        attrs = set_bit_at(attrs, 9, 1)
                    if not table_rw:
                        attrs = set_bit_at(attrs, 5, 1)
                    if not table_user:
                        attrs = set_bit_at(attrs, 4, 0)
                    if not lookup_secure:
                        attrs = set_bit_at(attrs, 3, 1)
            else:
                current_level += 1

        if bit_at(attrs, 8) == 0:
            taketohypmode = self.registers.current_mode_is_hyp() or not stage1
            ipavalid = not stage1
            self.data_abort(va, ia, domain, current_level, is_write, DAbort.ACCESS_FLAG, taketohypmode,
                            not stage1, ipavalid, ldfsr_format, s2fs1walk)
        result.perms.xn = bit_at(attrs, 12)
        result.perms.pxn = bit_at(attrs, 11)
        result.contiguousbit = bit_at(attrs, 10)
        result.ng = bit_at(attrs, 9)
        result.perms.ap = chain(substring(attrs, 5, 4), 1, 1)
        if stage1:
            result.addrdesc.memattrs = self.mair_decode(substring(attrs, 2, 0))
        else:
            result.addrdesc.memattrs = self.s2_attr_decode(substring(attrs, 3, 0))
        if result.addrdesc.memattrs.type == MemType.NORMAL:
            result.addrdesc.memattrs.shareable = bit_at(attrs, 7) == 0b1
            result.addrdesc.memattrs.outershareable = substring(attrs, 7, 6) == 0b10
        else:
            result.addrdesc.memattrs.shareable = True
            result.addrdesc.memattrs.outershareable = True
        result.domain = 0b0000  # unknown
        result.level = current_level
        result.blocksize = (512 ** (3 - current_level)) * 4
        result.addrdesc.paddress.physicaladdress = substring(output_address, 39, 0)
        if stage1:
            result.addrdesc.paddress.ns = bit_at(attrs, 3)
        else:
            result.addrdesc.paddress.ns = 1
        if stage1 and self.registers.current_mode_is_hyp():
            if bit_at(attrs, 4) != 0b1:
                print('unpredictable')
            if not table_user:
                print('unpredictable')
            if bit_at(attrs, 11) != 0b0:
                print('unpredictable')
            if not table_pxn:
                print('unpredictable')
            if bit_at(attrs, 9) != 0b0:
                print('unpredictable')
        return result

    def translation_table_walk_sd(self, mva, is_write, size):
        result = TLBRecord()
        l1descaddr = AddressDescriptor()
        l2descaddr = AddressDescriptor()
        taketohypmode = False
        ia = 0b0000000000000000000000000000000000000000  # unknown
        ipavalid = False
        stage2 = False
        ldfsr_format = False
        s2fs1walk = False
        domain = 0b0000  # unknown
        n = self.registers.ttbcr.n
        if n == 0 or substring(mva, 31, 32 - n) == 0:
            ttbr = self.registers.ttbr0_64
            disabled = self.registers.ttbcr.pd1 == 1
        else:
            ttbr = self.registers.ttbr1_64
            disabled = self.registers.ttbcr.pd1 == 1
            n = 0
        if have_security_ext() and disabled:
            level = 1
            self.data_abort(mva, ia, domain, level, is_write, DAbort.TRANSLATION, taketohypmode, stage2,
                            ipavalid, ldfsr_format, s2fs1walk)
        l1descaddr.paddress.physicaladdress = chain(substring(ttbr, 31, 14 - n), substring(mva, 31 - n, 20),
                                                    12 - n) << 2
        l1descaddr.paddress.ns = 0 if self.registers.is_secure() else 1
        l1descaddr.memattrs.type = MemType.NORMAL
        l1descaddr.memattrs.shareable = bit_at(ttbr, 1) == 1
        l1descaddr.memattrs.outershareable = bit_at(ttbr, 5) == 0 and bit_at(ttbr, 1) == 1
        hintsattrs = self.convert_attrs_hints(substring(ttbr, 4, 3))
        l1descaddr.memattrs.outerattrs = substring(hintsattrs, 1, 0)
        l1descaddr.memattrs.outerhints = substring(hintsattrs, 3, 2)
        if have_mp_ext():
            hintsattrs = self.convert_attrs_hints(chain(bit_at(ttbr, 0), bit_at(ttbr, 6), 1))
            l1descaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
            l1descaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
        else:
            if bit_at(ttbr, 0) == 0:
                hintsattrs = self.convert_attrs_hints(0b00)
                l1descaddr.memattrs.innerattrs = substring(hintsattrs, 1, 0)
                l1descaddr.memattrs.innerhints = substring(hintsattrs, 3, 2)
            else:
                l1descaddr.memattrs.innerattrs = (0b10
                                                  if configurations.translation_walk_sd_l1descaddr_attrs_10
                                                  else 0b11)
                l1descaddr.memattrs.innerhints = (0b01
                                                  if configurations.translation_walk_sd_l1descaddr_hints_01
                                                  else 0b11)
        if not have_virt_ext() or self.registers.is_secure():
            l1descaddr2 = l1descaddr
        else:
            l1descaddr2 = self.second_stage_translate(l1descaddr, mva, 4, is_write)
        l1desc = self.mem[l1descaddr2, 4]
        if self.registers.sctlr.ee:
            l1desc = big_endian_reverse(l1desc, 4)
        if substring(l1desc, 1, 0) == 0b00:
            level = 1
            self.data_abort(mva, ia, domain, level, is_write, DAbort.TRANSLATION, taketohypmode, stage2,
                            ipavalid, ldfsr_format, s2fs1walk)
        elif substring(l1desc, 1, 0) == 0b01:
            domain = substring(l1desc, 8, 5)
            level = 2
            pxn = bit_at(l1desc, 2)
            ns = bit_at(l1desc, 3)
            l2descaddr.paddress.physicaladdress = chain(substring(l1desc, 31, 10), substring(mva, 19, 12), 8) << 2
            l2descaddr.paddress.ns = 0 if self.registers.is_secure() else 1
            l2descaddr.memattrs = l1descaddr.memattrs
            if not have_virt_ext() or self.registers.is_secure():
                l2descaddr2 = l2descaddr
            else:
                l2descaddr2 = self.second_stage_translate(l2descaddr, mva, 4, is_write)
            l2desc = self.mem[l2descaddr2, 4]
            if self.registers.sctlr.ee:
                l2desc = big_endian_reverse(l2desc, 4)
            if substring(l2desc, 1, 0) == 0b00:
                self.data_abort(mva, ia, domain, level, is_write, DAbort.TRANSLATION, taketohypmode, stage2,
                                ipavalid, ldfsr_format, s2fs1walk)
            s = bit_at(l2desc, 10)
            ap = chain(bit_at(l2desc, 9), substring(l2desc, 5, 4), 2)
            ng = bit_at(l2desc, 11)
            if self.registers.sctlr.afe and bit_at(l2desc, 4) == 0:
                if not self.registers.sctlr.ha:
                    self.data_abort(mva, ia, domain, level, is_write, DAbort.ACCESS_FLAG, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.registers.sctlr.ee:
                        self.mem.set_bits(l2descaddr2, 4, 28, 1, 1)
                    else:
                        self.mem.set_bits(l2descaddr2, 4, 4, 1, 1)
            if bit_at(l2desc, 1) == 0:
                texcb = chain(substring(l2desc, 14, 12), substring(l2desc, 3, 2), 2)
                xn = bit_at(l2desc, 15)
                block_size = 64
                physicaladdressext = 0b00000000
                physicaladdress = chain(substring(l2desc, 31, 16), substring(mva, 15, 0), 16)
            else:
                texcb = chain(substring(l2desc, 8, 6), substring(l2desc, 3, 2), 2)
                xn = bit_at(l2desc, 0)
                block_size = 4
                physicaladdressext = 0b00000000
                physicaladdress = chain(substring(l2desc, 31, 12), substring(mva, 11, 0), 12)
        elif bit_at(l1desc, 1):
            texcb = chain(substring(l1desc, 14, 12), substring(l1desc, 3, 2), 2)
            s = bit_at(l1desc, 16)
            ap = chain(bit_at(l1desc, 15), substring(l1desc, 11, 10), 2)
            xn = bit_at(l1desc, 4)
            pxn = bit_at(l1desc, 0)
            ng = bit_at(l1desc, 17)
            level = 1
            ns = bit_at(l1desc, 19)
            if self.registers.sctlr.afe and bit_at(l1desc, 10) == 0:
                if not self.registers.sctlr.ha:
                    self.data_abort(mva, ia, domain, level, is_write, DAbort.ACCESS_FLAG, taketohypmode,
                                    stage2, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    if self.registers.sctlr.ee:
                        self.mem.set_bits(l1descaddr2, 4, 18, 1, 1)
                    else:
                        self.mem.set_bits(l1descaddr2, 4, 10, 1, 1)
            if bit_at(l1desc, 18) == 0:
                domain = substring(l1desc, 8, 5)
                block_size = 1024
                physicaladdressext = 0b00000000
                physicaladdress = chain(substring(l1desc, 31, 20), substring(mva, 19, 0), 20)
            else:
                domain = 0b0000
                block_size = 16384
                physicaladdressext = chain(substring(l1desc, 8, 5), substring(l1desc, 23, 20), 4)
                physicaladdress = chain(substring(l1desc, 31, 24), substring(mva, 23, 0), 24)
        if not self.registers.sctlr.tre:
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
        result.addrdesc.paddress.physicaladdress = chain(physicaladdressext, physicaladdress, 32)
        result.addrdesc.paddress.ns = ns if self.registers.is_secure() else 1
        return result

    def translate_address_v_s1_off(self, va):
        result = TLBRecord()
        if (not have_virt_ext() or
                not self.registers.hcr.dc or
                self.registers.is_secure() or
                self.registers.current_mode_is_hyp()):
            result.addrdesc.memattrs.type = MemType.STRONGLY_ORDERED
            result.addrdesc.memattrs.innerattrs = 0b00  # unknown
            result.addrdesc.memattrs.innerhints = 0b00  # unknown
            result.addrdesc.memattrs.outerattrs = 0b00  # unknown
            result.addrdesc.memattrs.outerhints = 0b00  # unknown
            result.addrdesc.memattrs.shareable = True
            result.addrdesc.memattrs.outershareable = True
        else:
            result.addrdesc.memattrs.type = MemType.NORMAL
            result.addrdesc.memattrs.innerattrs = 0b11
            result.addrdesc.memattrs.innerhints = 0b11
            result.addrdesc.memattrs.outerattrs = 0b11
            result.addrdesc.memattrs.outerhints = 0b11
            result.addrdesc.memattrs.shareable = False
            result.addrdesc.memattrs.outershareable = False
            if not self.registers.hcr.vm:
                print('unpredictable')
        result.perms.ap = 0b000  # unknown
        result.perms.xn = 0
        result.perms.pxn = 0
        result.ng = 0  # unknown
        result.domain = 0b0000  # unknown
        result.level = 0  # unknown
        result.blocksize = 0  # unknown
        result.addrdesc.paddress.physicaladdress = va
        result.addrdesc.paddress.ns = 0 if self.registers.is_secure() else 1
        return result

    def translate_address_v(self, va, ispriv, iswrite, size, wasaligned):
        s2fs1walk = False
        mva = self.fcse_translate(va)
        ishyp = self.registers.current_mode_is_hyp()
        if (ishyp and self.registers.hsctlr.m) or (not ishyp and self.registers.sctlr.m):
            if have_virt_ext() and not self.registers.is_secure() and not ishyp and self.registers.hcr.tge:
                print('unpredictable')
            uses_ld = ishyp or self.registers.ttbcr.eae
            if uses_ld:
                ia_in = mva
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
        if not wasaligned and tlbrecord_s1.addrdesc.memattrs.type in (MemType.STRONGLY_ORDERED, MemType.DEVICE):
            if not have_virt_ext():
                print('unpredictable')
            secondstageabort = False
            self.alignment_fault_v(mva, iswrite, ishyp, secondstageabort)
        if check_domain:
            check_permission = self.check_domain(tlbrecord_s1.domain, mva, tlbrecord_s1.level, iswrite)
        if check_permission:
            self.check_permission(
                tlbrecord_s1.perms, mva, tlbrecord_s1.level, tlbrecord_s1.domain, iswrite, ispriv, ishyp, uses_ld
            )
        if have_virt_ext() and not self.registers.is_secure() and not ishyp:
            if self.registers.hcr.vm:
                s1outputaddr = tlbrecord_s1.addrdesc.paddress.physicaladdress
                tlbrecord_s2 = self.translation_table_walk_ld(s1outputaddr, mva, iswrite, False, s2fs1walk, size)
                if (not wasaligned and
                        tlbrecord_s2.addrdesc.memattrs.type in (
                                MemType.DEVICE,
                                MemType.STRONGLY_ORDERED
                        )):
                    taketohypmode = True
                    secondstageabort = True
                    self.alignment_fault_v(mva, iswrite, taketohypmode, secondstageabort)
                self.check_permission_s2(tlbrecord_s2.perms, mva, s1outputaddr, tlbrecord_s2.level, iswrite, s2fs1walk)
                result = self.combine_s1s2_desc(tlbrecord_s1.addrdesc, tlbrecord_s2.addrdesc)
            else:
                result = tlbrecord_s1.addrdesc
        else:
            result = tlbrecord_s1.addrdesc
        return result

    def translate_address_p(self, va, ispriv, iswrite, wasaligned):
        result = AddressDescriptor()
        perms = Permissions()
        result.paddress.physicaladdress = va
        # IMPLEMENTATION_DEFINED setting of result.paddress.NS;
        if not self.registers.sctlr.m:
            result.memattrs = self.default_memory_attributes(va)
        else:
            region_found = False
            texcb = 0  # unknown
            s = False  # unknown
            for r in range(self.registers.mpuir.dregion):
                size_enable = self.registers.drsrs[r]
                base_address = self.registers.drbars[r]
                access_control = self.registers.dracrs[r]
                if size_enable.en:
                    ls_bit = size_enable.rsize + 1
                    if ls_bit < 2:
                        print('unpredictable')
                    if ls_bit > 2 and substring(base_address, ls_bit - 1, 2) != 0:
                        print('unpredictable')
                    if ls_bit == 32 or substring(va, 31, ls_bit) == substring(base_address, 31, ls_bit):
                        if ls_bit >= 8:
                            subregion = substring(va, ls_bit - 1, ls_bit - 3)
                            hit = size_enable.get_sd_n(subregion) == 0
                        else:
                            hit = True
                        if hit:
                            texcb = chain(chain(access_control.tex, access_control.c, 1), access_control.b, 1)
                            s = access_control.s
                            perms.ap = access_control.ap
                            perms.xn = access_control.xn
                            region_found = True
            if region_found:
                result.memattrs = self.default_tex_decode(texcb, s)
            else:
                if not self.registers.sctlr.br or not ispriv:
                    ipaddress = 0b0000000000000000000000000000000000000000  # unknown
                    domain = 0b0000  # unknown
                    level = 0  # unknown
                    taketohypmode = False
                    secondstageabort = False
                    ipavalid = False
                    ldfsr_format = False
                    s2fs1walk = False
                    self.data_abort(va, ipaddress, domain, level, iswrite, DAbort.BACKGROUND, taketohypmode,
                                    secondstageabort, ipavalid, ldfsr_format, s2fs1walk)
                else:
                    result.memattrs = self.default_memory_attributes(va)
                    perms.ap = 0b011
                    perms.xn = int(not self.registers.sctlr.v) if substring(va, 31, 28) == 0b1111 else bit_at(va, 31)
                    perms.pxn = 0
            if not wasaligned and result.memattrs.type in (MemType.DEVICE, MemType.STRONGLY_ORDERED):
                print('unpredictable')
            self.check_permission(perms, va, 0, 0b0000, iswrite, ispriv, False, False)
        return result

    def translate_address(self, va, ispriv, iswrite, size, wasaligned):
        if memory_system_architecture() == MemArch.VMSA:
            return self.translate_address_v(va, ispriv, iswrite, size, wasaligned)
        elif memory_system_architecture() == MemArch.PMSA:
            return self.translate_address_p(va, ispriv, iswrite, wasaligned)

    def is_exclusive_local(self, paddress, processorid, size):
        return False

    def is_exclusive_global(self, paddress, processorid, size):
        return False

    def clear_exclusive_local(self, processorid):
        pass

    def clear_exclusive_by_address(self, paddress, processorid, size):
        pass

    def mark_exclusive_global(self, paddress, processorid, size):
        pass

    def mark_exclusive_local(self, paddress, processorid, size):
        pass

    def bkpt_instr_debug_event(self):
        # mock
        raise NotImplementedError()

    def exclusive_monitors_pass(self, address, size):
        if address != align(address, size):
            self.alignment_fault(address, True)
        else:
            memaddrdesc = self.translate_address(address, self.registers.current_mode_is_not_user(), True, size, True)
        passed = self.is_exclusive_local(memaddrdesc.paddress, processor_id(), size)
        if passed:
            self.clear_exclusive_local(processor_id())
        if memaddrdesc.memattrs.shareable:
            passed = passed and self.is_exclusive_global(memaddrdesc.paddress, processor_id(), size)
        return passed

    def set_exclusive_monitors(self, address, size):
        memaddrdesc = self.translate_address(address, self.registers.current_mode_is_not_user(), False, size, True)
        if memaddrdesc.memattrs.shareable:
            self.mark_exclusive_global(memaddrdesc.paddress, processor_id(), size)
        self.mark_exclusive_local(memaddrdesc.paddress, processor_id(), size)

    def mem_a_with_priv_set(self, address, size, privileged, was_aligned, value):
        if address == align(address, size):
            va = address
        elif arch_version() >= 7 or self.registers.sctlr.a or self.registers.sctlr.u:
            self.alignment_fault(address, True)
        else:
            va = align(address, size)
        memaddrdesc = self.translate_address(va, privileged, True, size, was_aligned)
        if memaddrdesc.memattrs.shareable:
            self.clear_exclusive_by_address(memaddrdesc.paddress, processor_id(), size)
        if self.registers.cpsr.e:
            value = big_endian_reverse(value, size)
        self.mem[memaddrdesc, size] = value

    def mem_a_with_priv_get(self, address, size, privileged, was_aligned):
        if address == align(address, size):
            va = address
        elif arch_version() >= 7 or self.registers.sctlr.a or self.registers.sctlr.u:
            self.alignment_fault(address, False)
        else:
            va = align(address, size)
        memaddrdesc = self.translate_address(va, privileged, False, size, was_aligned)
        value = self.mem[memaddrdesc, size]
        if self.registers.cpsr.e:
            value = big_endian_reverse(value, size)
        return value

    def mem_a_set(self, address, size, value):
        self.mem_a_with_priv_set(address, size, self.registers.current_mode_is_not_user(), True, value)

    def mem_a_get(self, address, size):
        return self.mem_a_with_priv_get(address, size, self.registers.current_mode_is_not_user(), True)

    def mem_u_with_priv_set(self, address, size, privileged, value):
        if arch_version() < 7 and not self.registers.sctlr.a and not self.registers.sctlr.u:
            address = align(address, size)
        if address == align(address, size):
            self.mem_a_with_priv_set(address, size, privileged, True, value)
        elif (have_virt_ext() and
              not self.registers.is_secure() and
              self.registers.current_mode_is_hyp() and
              self.registers.hsctlr.a):
            self.alignment_fault(address, True)
        elif not self.registers.current_mode_is_hyp() and self.registers.sctlr.a:
            self.alignment_fault(address, True)
        else:
            if self.registers.cpsr.e:
                value = big_endian_reverse(value, size)
            for i in range(size):
                self.mem_a_with_priv_set(address + i, 1, privileged, False, substring(value, 8 * i + 7, 8 * i))

    def mem_u_with_priv_get(self, address, size, privileged):
        value = 0
        if arch_version() < 7 and not self.registers.sctlr.a and not self.registers.sctlr.u:
            address = align(address, size)
        if address == align(address, size):
            value = self.mem_a_with_priv_get(address, size, privileged, True)
        elif (have_virt_ext() and
              not self.registers.is_secure() and
              self.registers.current_mode_is_hyp() and
              self.registers.hsctlr.a):
            self.alignment_fault(address, False)
        elif not self.registers.current_mode_is_hyp() and self.registers.sctlr.a:
            self.alignment_fault(address, False)
        else:
            for i in range(size):
                value = set_substring(value, 8 * i + 7, 8 * i,
                                      self.mem_a_with_priv_get(address + i, 1, privileged, False))
            if self.registers.cpsr.e:
                value = big_endian_reverse(value, size)
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
        return self.registers.cpsr.e

    def unaligned_support(self):
        return self.registers.sctlr.u

    def hint_yield(self):
        # mock
        raise NotImplementedError()

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
        return is_armv7r_profile() and self.registers.sctlr.dz

    def generate_integer_zero_divide(self):
        raise UndefinedInstructionException("division by zero in the integer division instruction")

    def generate_coprocessor_exception(self):
        raise UndefinedInstructionException("rejected coprocessor instruction")

    def call_supervisor(self, immediate):
        if (self.registers.current_mode_is_hyp() or
                (have_virt_ext() and
                 not self.registers.is_secure() and
                 not self.registers.current_mode_is_not_user() and
                 self.registers.hcr.tge)):
            hsr_string = set_substring(0, 15, 0, immediate if self.current_cond() == 0b1110 else 0)
            self.write_hsr(0b010001, hsr_string)
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
            if have_security_ext():
                if not self.registers.is_secure() and not self.registers.nsacr.get_cp_n(cp_num):
                    raise UndefinedInstructionException()
            if not have_virt_ext() or not self.registers.current_mode_is_hyp():
                if self.registers.cpacr.get_cp_n(cp_num) == 0b00:
                    raise UndefinedInstructionException()
                elif self.registers.cpacr.get_cp_n(cp_num) == 0b01:
                    if not self.registers.current_mode_is_not_user():
                        raise UndefinedInstructionException()
                elif self.registers.cpacr.get_cp_n(cp_num) == 0b10:
                    print('unpredictable')
                elif self.registers.cpacr.get_cp_n(cp_num) == 0b11:
                    pass
            if have_security_ext() and have_virt_ext() and not self.registers.is_secure() and \
                    self.registers.hcptr.get_tcp_n(cp_num):
                hsr_string = 0b0000000000000000000000000
                hsr_string = set_substring(hsr_string, 3, 0, cp_num & 0xF)
                self.write_hsr(0b000111, hsr_string)
                if not self.registers.current_mode_is_hyp():
                    self.registers.take_hyp_trap_exception()
                else:
                    raise UndefinedInstructionException()
            return self.cpx_instr_decode(instr)
        elif cp_num == 14:
            two_reg = False
            if substring(instr, 27, 24) == 0b1110 and bit_at(instr, 4) and substring(instr, 31, 28) != 0b1111:
                opc1 = substring(instr, 23, 21)
                two_reg = False
            elif substring(instr, 27, 20) == 0b11000101 and substring(instr, 31, 28) != 0b1111:
                opc1 = substring(instr, 7, 4)
                if opc1 != 0:
                    raise UndefinedInstructionException()
                two_reg = True
            elif substring(instr, 27, 25) == 0b110 and substring(instr, 31, 28) != 0b1111:
                opc1 = 0
                if substring(instr, 15, 12) != 5:
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
                if substring(instr, 7, 5) != 0b000 or substring(instr, 3, 1) != 0b000 or substring(instr, 15,
                                                                                                   12) == 0b1111:
                    print('unpredictable')
                else:
                    if bit_at(instr, 0) == 0:
                        if not self.registers.current_mode_is_not_user():
                            raise UndefinedInstructionException()
                    if bit_at(instr, 1) == 1:
                        if not self.registers.current_mode_is_not_user() and self.registers.teecr.xed:
                            raise UndefinedInstructionException()
                    if (have_security_ext() and
                            have_virt_ext() and
                            not self.registers.is_secure() and
                            not self.registers.current_mode_is_hyp() and
                            self.registers.hstr.ttee):
                        hsr_string = 0b0000000000000000000000000
                        hsr_string = set_substring(hsr_string, 19, 17, substring(instr, 7, 5))
                        hsr_string = set_substring(hsr_string, 16, 14, substring(instr, 23, 21))
                        hsr_string = set_substring(hsr_string, 13, 10, substring(instr, 19, 16))
                        hsr_string = set_substring(hsr_string, 8, 5, substring(instr, 15, 12))
                        hsr_string = set_substring(hsr_string, 4, 1, substring(instr, 3, 0))
                        self.write_hsr(0b000101, hsr_string)
                        self.registers.take_hyp_trap_exception()
                return True
            elif opc1 == 7:
                return self.cp14_jazelle_instr_decode(instr)
            else:
                raise UndefinedInstructionException()
        elif cp_num == 15:
            if substring(instr, 27, 24) == 0b1110 and bit_at(instr, 4) and substring(instr, 31, 28) != 0b1111:
                cr_nnum = substring(instr, 19, 16)
                two_reg = False
            elif substring(instr, 27, 21) == 0b1100010 and substring(instr, 31, 28) != 0b1111:
                cr_nnum = substring(instr, 3, 0)
                two_reg = True
            else:
                raise UndefinedInstructionException()
            if cr_nnum == 4:
                print('unpredictable')
            if (have_security_ext() and
                    have_virt_ext() and
                    not self.registers.is_secure() and
                    not self.registers.current_mode_is_hyp() and
                    cr_nnum != 14 and
                    self.registers.hstr.get_t_n(cr_nnum)):
                if not self.registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
                    if configurations.coproc_accepted_pl0_undefined:
                        raise UndefinedInstructionException()
                hsr_string = 0b0000000000000000000000000
                if two_reg:
                    hsr_string = set_substring(hsr_string, 19, 16, substring(instr, 7, 4))
                    hsr_string = set_substring(hsr_string, 13, 10, substring(instr, 19, 16))
                    hsr_string = set_substring(hsr_string, 8, 5, substring(instr, 15, 12))
                    hsr_string = set_substring(hsr_string, 4, 1, substring(instr, 3, 0))
                    hsr_string = set_bit_at(hsr_string, 0, bit_at(instr, 20))
                    self.write_hsr(0b000100, hsr_string)
                else:
                    hsr_string = set_substring(hsr_string, 19, 17, substring(instr, 7, 5))
                    hsr_string = set_substring(hsr_string, 16, 14, substring(instr, 23, 21))
                    hsr_string = set_substring(hsr_string, 13, 10, substring(instr, 19, 16))
                    hsr_string = set_substring(hsr_string, 8, 5, substring(instr, 15, 12))
                    hsr_string = set_substring(hsr_string, 4, 1, substring(instr, 3, 0))
                    hsr_string = set_bit_at(hsr_string, 0, bit_at(instr, 20))
                    self.write_hsr(0b000011, hsr_string)
                self.registers.take_hyp_trap_exception()
            if (have_security_ext() and
                    have_virt_ext() and
                    not self.registers.is_secure() and
                    not self.registers.current_mode_is_hyp() and
                    self.registers.hcr.tidcp and
                    not two_reg):
                cr_mnum = substring(instr, 3, 0)
                if (cr_nnum == 9 and cr_mnum in (0, 2, 5, 6, 7, 8)) or (
                        cr_nnum == 10 and cr_mnum in (0, 1, 4, 8)) or (
                        cr_nnum == 11 and cr_mnum in (0, 1, 2, 3, 4, 5, 6, 7, 8, 15)):
                    if not self.registers.current_mode_is_not_user() and self.instr_is_pl0_undefined(instr):
                        if configurations.coproc_accepted_pl0_undefined:
                            raise UndefinedInstructionException()
                        hsr_string = 0b0000000000000000000000000
                        hsr_string = set_substring(hsr_string, 19, 17, substring(instr, 7, 5))
                        hsr_string = set_substring(hsr_string, 16, 14, substring(instr, 23, 21))
                        hsr_string = set_substring(hsr_string, 13, 10, substring(instr, 19, 16))
                        hsr_string = set_substring(hsr_string, 8, 5, substring(instr, 15, 12))
                        hsr_string = set_substring(hsr_string, 4, 1, substring(instr, 3, 0))
                        hsr_string = set_bit_at(hsr_string, 0, bit_at(instr, 20))
                        self.write_hsr(0b000011, hsr_string)
                        self.registers.take_hyp_trap_exception()
            return self.cp15_instr_decode(instr)

    def coproc_get_word_to_store(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_done_storing(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_done_loading(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_send_loaded_word(self, word, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_send_two_words(self, word2, word1, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_get_two_words(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_internal_operation(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_send_one_word(self, word, cp_num, instr):
        # mock
        raise NotImplementedError()

    def coproc_get_one_word(self, cp_num, instr):
        # mock
        raise NotImplementedError()

    def hint_preload_data_for_write(self, address):
        # mock
        raise NotImplementedError()

    def hint_preload_data(self, address):
        # mock
        raise NotImplementedError()

    def data_synchronization_barrier(self, domain, types):
        # mock
        raise NotImplementedError()

    def instruction_synchronization_barrier(self):
        # mock
        raise NotImplementedError()

    def in_it_block(self):
        return lower_chunk(self.registers.cpsr.it, 4) != 0b0000

    def last_in_it_block(self):
        return lower_chunk(self.registers.cpsr.it, 4) == 0b1000

    def increment_pc_if_needed(self):
        if not self.registers.changed_registers[15]:
            self.registers.increment_pc(self.this_instr_length() // 8)

    def emulate_cycle(self):
        try:
            instr = self.fetch_instruction()
            opcode_c = self.decode_instruction(instr)
            if not opcode_c:
                raise UndefinedInstructionException()
            opcode_c = opcode_c.from_bitarray(instr, self)
            self.execute_instruction(opcode_c)
            self.increment_pc_if_needed()
        except EndOfInstruction:
            pass
        except SVCException:
            self.registers.take_svc_exception()
        except SMCException:
            self.registers.take_smc_exception()
        except DataAbortException as dabort_exception:
            self.registers.take_data_abort_exception(dabort_exception)
        except HypTrapException:
            self.registers.take_hyp_trap_exception()
        except UndefinedInstructionException:
            self.registers.take_undef_instr_exception()

    def fetch_instruction(self):
        if self.registers.current_instr_set() == InstrSet.ARM:
            self.opcode_len = 4
            self.opcode = self.mem_a_get(self.registers.pc_store_value(), self.opcode_len)
        elif self.registers.current_instr_set() == InstrSet.THUMB:
            self.opcode_len = 2
            self.opcode = self.mem_a_get(self.registers.pc_store_value(), self.opcode_len)
            opcode_start = substring(self.opcode, 15, 11)
            if opcode_start in (0b11101, 0b11110, 0b11111):
                self.opcode_len += 2
                new_part = self.mem_a_get(add(self.registers.pc_store_value(), 2, 32), 2)
                self.opcode = chain(self.opcode, new_part, 16)
        self.opcode_len *= 8
        return self.opcode

    def decode_instruction(self, instr):
        return op_decode_instruction(instr, self)

    def execute_instruction(self, opcode):
        self.registers.changed_registers = [False] * 16
        self.executed_opcode = opcode
        if self.in_it_block():
            opcode.execute(self)
            self.registers.it_advance()
        else:
            opcode.execute(self)
