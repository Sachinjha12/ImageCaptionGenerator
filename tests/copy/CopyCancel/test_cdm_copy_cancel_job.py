from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.ssh import SSH


import pytest

payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    'copies': 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after init
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_job_cancel_flatbed_after_init_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_job_cancel_flatbed_after_init_cdm_and_state_changes
        +guid: 1db29b77-2e57-46ad-8b32-3f9f6517f480
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_job_cancel_flatbed_after_init_cdm_and_state_changes(cdm, udw):
        payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    "copies": 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

        Copy(cdm, udw).do_copy_job(cancel = Cancel.after_init, **payload)

    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after start
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cancel_adf_after_start_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cancel_adf_after_start_cdm_and_state_changes
        +guid: d81f67cb-d098-4002-bfe7-f436e1807244
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cancel_adf_after_start_cdm_and_state_changes(cdm, udw, scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(cancel = Cancel.after_start, **payload)
    scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after init
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cancel_adf_after_init_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cancel_adf_after_init_cdm_and_state_changes
        +guid: 63396277-69f6-41a2-9c1d-567ba9f1c10d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cancel_adf_after_init_cdm_and_state_changes(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(cancel = Cancel.after_init, **payload)
    scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after start
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cancel_flatbed_after_start_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cancel_flatbed_after_start_cdm_and_state_changes
        +guid: a268bbad-a803-4047-9187-ad02e1148d35
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cancel_flatbed_after_start_cdm_and_state_changes(cdm, udw):
        Copy(cdm, udw).do_copy_job(cancel = Cancel.after_start, **payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after init
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cancel_flatbed_after_init_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cancel_flatbed_after_init_cdm_and_state_changes
        +guid: 6d7be720-e8da-49f7-aa28-f9c217467f3e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cancel_flatbed_after_init_cdm_and_state_changes(cdm, udw):
        Copy(cdm, udw).do_copy_job(cancel = Cancel.after_init, **payload)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after start
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_job_cancel_adf_after_start_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_job_cancel_adf_after_start_cdm_and_state_changes
        +guid: c2b8d62f-dd9d-4fa5-bda4-93d469069945
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_job_cancel_adf_after_start_cdm_and_state_changes(cdm, udw,scan_emulation):
    if cdm.device_feature_cdm.is_color_supported():      
        color_mode = 'color'
    else:
        color_mode = 'grayscale'
    payload = {
            'src': {
                'scan': {
                    'colorMode':color_mode,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    "copies": 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(cancel = Cancel.after_start, **payload)
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    # scan_emulation.media.unload_media('ADF')

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy cancel after init
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_cdm_job_cancel_adf_after_init_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Negative
    +test:
        +title: test_copy_cdm_job_cancel_adf_after_init_state_changes
        +guid: 44de3390-1361-4c7b-89aa-cbaf1da667da
        +dut:
            +type:Simulator
            +configuration: ScannerInput=AutomaticDocumentFeeder & DeviceClass=MFP & DeviceFunction=Copy

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_job_cancel_adf_after_init_state_changes(cdm,udw,scan_emulation):
    if cdm.device_feature_cdm.is_color_supported():      
        color_mode = 'color'
    else:
        color_mode = 'grayscale'
    payload = {
            'src': {
                'scan': {
                    'colorMode':color_mode,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                },
            },
            'dest': {
                'print': {
                    "copies": 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(cancel = Cancel.after_init, **payload)
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    # scan_emulation.media.unload_media('ADF')
 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify mutilple copy job cancel state with copies.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-161363
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_multiple_job_canceled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_multiple_job_canceled
        +guid: 17d6707c-4c62-4674-afa6-86b64575e48f
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanOriginalSides=2-sided & ADFResolution=600dpi
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_multiple_job_canceled(cdm, udw, job, scan_emulation):
    job.clear_joblog()
    try:
        payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                    'resolution':'e600Dpi',
                },
            },
            'dest': {
                'print': {
                    "copies": 2,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                }
            }
        }
        udw.mainApp.ScanDeviceService.setNumScanPages(10)
        scan_emulation.media.load_media('ADF')
        copyjob_id_one =Copy(cdm, udw).do_copy_job(cancel = Cancel.submit_and_exit)
        job.cancel_job(copyjob_id_one)
        copyjob_id_two =Copy(cdm, udw).do_copy_job(cancel = Cancel.submit_and_exit)
        job.cancel_job(copyjob_id_two)
        job.check_job_log_by_status_and_type_cdm(
        completion_state_list=[
            {"type": "copy", "status": "cancelled"},
            {"type": "copy", "status": "cancelled"}])

    finally:
        udw.mainApp.ScanDeviceService.setNumScanPages(1)