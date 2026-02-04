from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job nup
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_simple_flatbed_2up_grayscale
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_simple_flatbed_2up_grayscale
        +guid: 8b1abecd-de96-48dd-8365-dc914e0c066b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_simple_flatbed_2up_grayscale(cdm, udw):
    payload = {
            'src': {
                'scan': {
                    'colorMode':'Grayscale',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'pagesPerSheet':'TwoUp',
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

    Copy(cdm, udw).do_copy_job(**payload)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple copy job nup best
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-9875
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_simple_flatbed_2up_best
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_simple_flatbed_2up_best
        +guid: 4687bd97-e19c-4443-866a-04f797d95f7f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_cdm_simple_flatbed_2up_best(cdm, udw):
    payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'pagesPerSheet':'TwoUp',
                },
            },
            'dest': {
                'print': {
                    'copies': 10,
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'printQuality' : 'best',
                }
            }
        }

    Copy(cdm, udw).do_copy_job(**payload)
