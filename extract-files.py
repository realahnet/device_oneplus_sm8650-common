#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm8650-common',
    'hardware/qcom-caf/sm8650',
    'hardware/qcom-caf/wlan',
    'hardware/oplus',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'com.qti.sensor.lyt808',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccsyshal@1.2',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
    (
        'libagmclient',
        'libpalclient',
        'libar-acdb',
        'libar-gsl',
        'libats',
        'liblx-osal',
        'liblx-ar_util',
        'vendor.qti.hardware.AGMIPC@1.0-impl',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'odm/bin/hw/android.hardware.secure_element-service.qti',
        'vendor/lib64/qcrilNr_aidl_SecureElementService.so',
    ): blob_fixup()
        .replace_needed('android.hardware.secure_element-V1-ndk.so', 'android.hardware.secure_element-V1-ndk_odm.so'),
    'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff': blob_fixup()
        .add_needed('libshims_aidl_fingerprint_v3.oplus.so')
        .replace_needed('libtinyxml2.so', 'libtinyxml2_stock.so'),
    'odm/etc/init/vendor.oplus.hardware.biometrics.fingerprint@2.1-service.rc': blob_fixup()
        .regex_replace(r'(group system input uhid\n)', r'\1    task_profiles ProcessCapacityHigh MaxPerformance\n'),
    'odm/etc/init/init.touchDaemon.rc': blob_fixup()
        .regex_replace(r'(group root inet misc sdcard_rw sdcard_r media_rw system radio input system\n)', r'\1    task_profiles ProcessCapacityHigh MaxPerformance\n',
    ),
    'odm/etc/permissions/vendor-oplus-hardware-charger.xml': blob_fixup()
        .regex_replace('/system/system_ext', '/system_ext'),
    'vendor/etc/seccomp_policy/gnss@2.0-qsap-location.policy': blob_fixup()
        .add_line_if_missing('sched_get_priority_min: 1')
        .add_line_if_missing('sched_get_priority_max: 1'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'system_ext/bin/horae': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite.so', 'libprotobuf-cpp-lite-21.7.so'),
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so': blob_fixup()
        .replace_needed('libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.7.so'),
    (
        'vendor/bin/qvrdatauploader',
        'odm/bin/hw/vendor-oplus-hardware-touch-V2-service',
        'odm/bin/touchDaemon',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2_stock.so'),
    (
        'vendor/lib64/libcapiv2uvvendor.so',
        'vendor/lib64/liblistensoundmodel2vendor.so',
        'vendor/lib64/libVoiceSdk.so',
    ): blob_fixup()
        .replace_needed('libtensorflowlite_c.so', 'libtensorflowlite_c_vendor.so'),
    'vendor/bin/init.kernel.post_boot-memory.sh': blob_fixup()
        .regex_replace('# echo always', 'echo always'),
    'vendor/bin/system_dlkm_modprobe.sh': blob_fixup()
        .regex_replace(r'(?m)^.*zram or zsmalloc.*\n?', '')
        .regex_replace('-e "zram" -e "zsmalloc"', ''),
    (
        'vendor/etc/media_codecs_pineapple.xml',
        'vendor/etc/media_codecs_pineapple_vendor.xml',
        'vendor/etc/media_codecs_cliffs_v0.xml',
    ): blob_fixup()
        .regex_replace(r'(?m)^.*media_codecs_(?:google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n?', ''),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    (
        'vendor/lib64/libqcrilNr.so',
        'vendor/lib64/libril-db.so',
    ): blob_fixup()
        .regex_replace('persist.vendor.radio.poweron_opt', 'persist.vendor.radio.poweron_ign'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libhidlbase_shim.so'),
    (
        'vendor/bin/qcc-vendor',
        'vendor/bin/qms',
        'vendor/bin/xtra-daemon',
        'vendor/lib64/libqms_client.so',
        'vendor/lib64/libqcc_sdk.so',
        'vendor/lib64/libcne.so',
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    'vendor/etc/public.libraries.txt': blob_fixup()
        .add_line_if_missing('libarcsoft_hdr_couple_api.so')
        .add_line_if_missing('libarcsoft_high_dynamic_range_couple.so')
        .add_line_if_missing('libarcsoft_smart_denoise.so')
        .add_line_if_missing('libarcsoft_turbo_hdr_raw.so')
        .add_line_if_missing('libarcsoft_turbo_raw.so')
        .add_line_if_missing('libarcsoft_qnnhtp.so')
        .add_line_if_missing('libQnnHtp.so')
        .add_line_if_missing('libQnnSystem.so')
        .add_line_if_missing('libQnnHtpV75Stub.so')
        .add_line_if_missing('libQnnGpu.so')
        .add_line_if_missing('libQnnHtpStub.so'),
    'system_ext/etc/seccomp_policy/tcmd.policy': blob_fixup()
        .add_line_if_missing('lseek: 1')
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8650-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
