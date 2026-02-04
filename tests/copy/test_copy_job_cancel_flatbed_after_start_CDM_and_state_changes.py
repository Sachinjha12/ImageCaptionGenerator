from dunetuf.copy.copy import *


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
    +name: test_copy_job_cancel_flatbed_after_start_cdm_and_state_changes
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_job_cancel_flatbed_after_start_cdm_and_state_changes
        +guid: 959d2f68-fcab-4994-883a-c68a75f7a5bc
        +dut:
            +type:Simulator
            +configuration: ScannerInput=Flatbed & DeviceClass=MFP

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_job_cancel_flatbed_after_start_cdm_and_state_changes(cdm, udw, scan_emulation, configuration):
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
    scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_job(cancel = Cancel.after_start, familyname = configuration.familyname, **payload)
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    scan_emulation.media.load_media('ADF',1)
