from enum import Enum

MemArch = Enum("MemArch", "MemArch_VMSA MemArch_PMSA")
MBReqDomain = Enum(
        "MBReqDomain",
        "MBReqDomain_FullSystem MBReqDomain_OuterShareable MBReqDomain_InnerShareable MBReqDomain_Nonshareable"
)
MBReqTypes = Enum("MBReqTypes", "MBReqTypes_All MBReqTypes_Writes")
InstrSet = Enum("InstrSet", "InstrSet_ARM InstrSet_Thumb InstrSet_Jazelle InstrSet_ThumbEE")
DAbort = Enum("DAbort", ("DAbort_AccessFlag DAbort_Alignment DAbort_Background DAbort_Domain DAbort_Permission "
                         "DAbort_Translation DAbort_SyncExternal DAbort_SyncExternalonWalk DAbort_SyncParity "
                         "DAbort_SyncParityonWalk DAbort_AsyncParity DAbort_AsyncExternal DAbort_SyncWatchpoint "
                         "DAbort_AsyncWatchpoint DAbort_TLBConflict DAbort_Lockdown DAbort_Coproc DAbort_ICacheMaint"))
