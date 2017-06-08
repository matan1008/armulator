import json
from armulator.enums import *

with open("armulator/arm_configurations.json") as f:
    configurations = json.load(f)

number_of_mpu_regions = configurations["number_of_mpu_regions"]


def have_security_ext():
    return configurations["have_security_ext"]


def have_virt_ext():
    return configurations["have_virt_ext"]


def arch_version():
    return configurations["arch_version"]


def jazelle_accepts_execution():
    return configurations["jazelle_accepts_execution"]


def memory_system_architecture():
    return {"PMSA": MemArch.MemArch_PMSA, "VMSA": MemArch.MemArch_VMSA}[configurations["memory_system_architecture"]]


def have_lpae():
    return configurations["have_lpae"]


def have_mp_ext():
    return configurations["have_mp_ext"]


def have_adv_simd_or_vfp():
    return configurations["have_adv_simd_or_vfp"]


def have_thumbee():
    return configurations["have_thumbee"]


def have_jazelle():
    return configurations["have_jazelle"]


def implementation_supports_transient():
    return configurations["implementation_supports_transient"]


def processor_id():
    return configurations["processor_id"]


def is_armv7r_profile():
    return configurations["is_armv7r_profile"]


def has_imp_def_reset_vector():
    return configurations["has_imp_def_reset_vector"]
