from dunetuf.copy.copy import *
import pytest


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: multiple copy with flatbed
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17183
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns    
    +name: test_copy_cdm_multiple_job_flatbed_simplex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_multiple_job_flatbed_simplex
        +guid:a8fa743a-a90c-466c-a8ef-97a2abffc21b
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_multiple_job_flatbed_simplex(cdm, udw):
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
                    'copies': 5,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }
    Copy(cdm, udw).do_copy_job(**payload)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: multiple copy with ADF
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17183
    +timeout:120
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +asset: Copy
    +test_framework: TUF
    +name: test_copy_cdm_multiple_job_adf_simplex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_multiple_job_adf_simplex
        +guid:de6440f5-b61b-4146-a11d-c703530c066c
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_multiple_job_adf_simplex(cdm, udw, scan_emulation):
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
                    'copies': 5,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                }
            }
        }
    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: simplex copy to duplex
    +test_tier: 1
    +is_manual: False
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_classification:System
    +reqid: DUNE-17184
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +name: test_copy__simplex_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy__simplex_duplex_using_cdm
        +guid:d104e931-d93c-4be6-b965-812bef07ef3a
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanColorMode=Automatic
             
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy__simplex_duplex_using_cdm(cdm, udw,scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'colorMode':'Automatic',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
                }
            }
        }
    scan_emulation.media.load_media('ADF',6)
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name: test_copy_cdm_simple_adf_duplex
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_simple_adf_duplex
        +guid:0e18eb6b-d41f-4201-b7a5-14918112d3d0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_simple_adf_duplex(cdm, udw, scan_emulation):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'duplex',
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

    scan_emulation.media.load_media('ADF',1)
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
 
 