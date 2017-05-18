from enum import Enum

MemArch = Enum("MemArch", "MemArch_VMSA MemArch_PMSA")
MBReqDomain = Enum(
        "MBReqDomain",
        "MBReqDomain_FullSystem MBReqDomain_OuterShareable MBReqDomain_InnerShareable MBReqDomain_Nonshareable"
)
MBReqTypes = Enum("MBReqTypes", "MBReqTypes_All MBReqTypes_Writes")
InstrSet = Enum("InstrSet", "InstrSet_ARM InstrSet_Thumb InstrSet_Jazelle InstrSet_ThumbEE")
