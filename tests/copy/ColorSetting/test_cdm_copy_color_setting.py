from dunetuf.copy.copy import *

import pytest

payload = {
            'src': {
                'scan': {
                    'colorMode':'color',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: color multiple page copy from ADF
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17182
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_color_adf_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_color_adf_duplex_using_cdm
        +guid:99a86138-cc6c-493b-896b-75c7c575491e
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & ScannerInput=AutomaticDocumentFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_adf_duplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',5)
    payload['dest']['print']['plexMode'] = 'duplex'
    Copy(cdm, udw).do_copy_job(**payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: grayscale single page copy from flatbed
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17182
    +timeout:200
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_grayscale_flatbed_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_grayscale_flatbed_simplex_using_cdm
        +guid:804d0d6d-52f8-4f4a-a149-a3f78585327f
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_grayscale_flatbed_simplex_using_cdm(cdm, udw,):
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    payload['src']['scan']['colorMode'] = 'grayscale'
    payload['dest']['print']['plexMode'] = 'simplex'
    Copy(cdm, udw).do_copy_job(**payload, waitTime=90)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: grayscale multiple page copy from ADF
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17182
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_grayscale_adf_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_grayscale_adf_duplex_using_cdm
        +guid:9e7a95d6-cc88-4410-8f79-38218fcfadf6
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_grayscale_adf_duplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',5)
    payload['src']['scan']['colorMode'] = 'grayscale'
    payload['dest']['print']['plexMode'] = 'duplex'
    Copy(cdm, udw).do_copy_job(**payload)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Auto color mode single page copy from flatbed
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_color_autodetect_flatbed_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_color_autodetect_flatbed_simplex_using_cdm
        +guid:4c6812a7-bee6-428f-ad6b-3fdeb777e6d8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_autodetect_flatbed_simplex_using_cdm(cdm, udw):
    udw.mainApp.ScanDeviceService.setNumScanPages(1)
    if cdm.device_feature_cdm.is_color_supported():
        payload['src']['scan']['colorMode'] = 'autoDetect'
    payload['dest']['print']['plexMode'] = 'simplex'
    Copy(cdm, udw).do_copy_job(**payload)    

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:color mode autodetect multiple page copy from ADF
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_color_autodetect_adf_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_color_autodetect_adf_duplex_using_cdm
        +guid:9b74f4ac-4739-4636-84c9-5918b493a0f4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_autodetect_adf_duplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',3)
    if cdm.device_feature_cdm.is_color_supported():
        payload['src']['scan']['colorMode'] = 'autoDetect'
    payload['dest']['print']['plexMode'] = 'duplex'
    Copy(cdm, udw).do_copy_job(**payload)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: color single page copy from flatbed
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17182
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_color_flatbed_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_color_flatbed_simplex_using_cdm
        +guid:eb6ccea8-d928-4b2d-a01a-0c9577ec6c83
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_flatbed_simplex_using_cdm(cdm, udw):
    Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload)
