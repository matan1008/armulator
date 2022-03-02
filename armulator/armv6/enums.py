from enum import Enum, auto

__all__ = ['MemArch', 'MBReqDomain', 'MBReqTypes', 'InstrSet', 'DAbort']


class MemArch(Enum):
    VMSA = auto()
    PMSA = auto()


class MBReqDomain(Enum):
    FULL_SYSTEM = auto()
    OUTER_SHAREABLE = auto()
    INNER_SHAREABLE = auto()
    NONSHAREABLE = auto()


class MBReqTypes(Enum):
    ALL = auto()
    WRITES = auto()


class InstrSet(Enum):
    ARM = 0b00
    THUMB = 0b01
    JAZELLE = 0b10
    THUMB_EE = 0b11


class DAbort(Enum):
    ACCESS_FLAG = auto()
    ALIGNMENT = auto()
    BACKGROUND = auto()
    DOMAIN = auto()
    PERMISSION = auto()
    TRANSLATION = auto()
    SYNC_EXTERNAL = auto()
    SYNC_EXTERNAL_ON_WALK = auto()
    SYNC_PARITY = auto()
    SYNC_PARITY_ON_WALK = auto()
    ASYNC_PARITY = auto()
    ASYNC_EXTERNAL = auto()
    SYNC_WATCHPOINT = auto()
    ASYNC_WATCHPOINT = auto()
    TLB_CONFLICT = auto()
    LOCKDOWN = auto()
    COPROC = auto()
    ICACHE_MAINT = auto()
