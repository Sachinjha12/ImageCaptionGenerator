from dunetuf.copy.copy import *
import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview job
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-53710
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_preview_using_CDM
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_preview_using_CDM
        +guid:e2fc65e9-451b-442e-86d1-0744f37c9813
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator     
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_preview_using_CDM(cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'mediaSource':'flatbed'
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    loaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    if loaded:
        print('ADF is loaded, unloading for flatbed job')
        scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_preview_job(cancel = Cancel.no, reps = 1, **payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview job with prescan
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-53710
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_preview__using_CDM_Prescan
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_preview__using_CDM_Prescan
        +guid:589533fd-0e2b-4017-97af-4d21d50709dc
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter & FlatbedMediaSize=AnySize
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator     
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_preview__using_CDM_Prescan(cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'any',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'mediaSource':'flatbed'
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    loaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    if loaded:
        print('ADF is loaded, unloading for flatbed job')
        scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_preview_job(cancel = Cancel.no, reps = 1, **payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview job, with multiple previews
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-53710
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_preview__with_multiple_previews
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_preview__with_multiple_previews
        +guid:c413ba13-0745-45c9-bd28-1ca43732c176
        +dut: 
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
    
def test_copy_preview__with_multiple_previews(cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'mediaSource':'flatbed'
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    loaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    if loaded:
        print('ADF is loaded, unloading for flatbed job')
        scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_preview_job(cancel = Cancel.no, reps = 3, **payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy preview job, cancel after the preview
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-53710
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_preview_with_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_preview_with_cancel
        +guid:3fbaa35c-4343-48c2-a544-8cec0baeea2b
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_preview_with_cancel(cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'mediaSource':'flatbed'
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }

    loaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    if loaded:
        print('ADF is loaded, unloading for flatbed job')
        scan_emulation.media.unload_media('ADF')
    Copy(cdm, udw).do_copy_preview_job(cancel = Cancel.after_preview, reps = 1, **payload)
