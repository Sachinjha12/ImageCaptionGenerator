from dunetuf.copy.copy import *
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
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_simple_job_flatbed_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_simple_job_flatbed_using_cdm
        +guid: ff774ac4-b6d0-4cec-972b-02a24a74179b
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

def test_copy_simple_job_flatbed_using_cdm(setup_teardown_with_copy_job, cdm, udw,scan_emulation):
    try:
        scan_emulation.media.unload_media('ADF')
        Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload, waitTime=600)

    finally:
        scan_emulation.media.load_media('ADF')
    
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_simple_job_adf_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_simple_job_adf_simplex_using_cdm
        +guid: 1e5d2a7f-6167-4b77-9247-1630e5f6079e
        +dut:
            +type:Simulator
            +configuration: ScannerInput=AutomaticDocumentFeeder & DeviceClass=MFP & DeviceFunction=Copy

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_simple_job_adf_simplex_using_cdm(cdm, udw, scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(**payload, waitTime=600)
    scan_emulation.media.unload_media('ADF')
