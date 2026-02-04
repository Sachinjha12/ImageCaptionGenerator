from dunetuf.copy.copy import *

#------------------------------------------------------------------------------
# Parse the command line arguments
#------------------------------------------------------------------------------

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug",
                  action="store_true", default=False,
                  help="Print debug messages to stdout")
parser.add_argument("-v", "--verbose",
                  action="store_true", default=False,
                  help="Print info messages to stdout")
args,unknown_args = parser.parse_known_args()

#------------------------------------------------------------------------------
# Set up logging
#------------------------------------------------------------------------------

import logging
logSeparator = '---------------------'
logFormat = '[%(asctime)s] %(levelname)s "%(message)s" (%(name)s)'
logDateFormat = "%d/%b/%Y %H:%M:%S"
if args.debug:
    logLevel = logging.DEBUG
elif args.verbose:
    logLevel = logging.INFO
else:
    logLevel = logging.ERROR
logging.basicConfig(level=logLevel,format=logFormat,datefmt=logDateFormat)
log = logging.getLogger("test_cdm_trayconfig")


payload = {
            'src': {
                'scan': {
                    'colorMode':'color',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'contentType':'mixed',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSource': 'auto',
                    'mediaSize':'na_letter_8.5x11in',
                    'mediaType': 'stationery',
                    'plexMode':'simplex',
                    'printQuality' : 'normal',
                }
            },
            'pipelineOptions': {
                'imageModifications': {
                    'exposure': 5,
                },
                'scaling': {
                    'xScalePercent': 100,
                    'yScalePercent': 100,
                }

            }
        }

def reset_payload():
    payload = {
            'src': {
                'scan': {
                    'colorMode':'color',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                    'resolution':'e300Dpi',
                    'contentType':'mixed',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSource': 'auto',
                    'mediaSize':'na_letter_8.5x11in',
                    'mediaType': 'stationery',
                    'plexMode':'simplex',
                    'printQuality' : 'normal',
                }
            },
            'pipelineOptions': {
                'imageModifications': {
                    'exposure': 5,
                },
                'scaling': {
                    'xScalePercent': 100,
                    'yScalePercent': 100,
                }

            }
        }

payload1 = {
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Testing the content type options from the copy menu
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-34810
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_settings_contenttype
    +test:
        +title: test_copy_cdm_settings_contenttype
        +guid:a408a4a4-c1bd-4d51-a301-dc6413c68e3c
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & FlatbedMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_settings_contenttype(cdm, udw,scan_emulation):
    scan_emulation.media.unload_media('ADF')
    if not cdm.device_feature_cdm.is_color_supported():
        payload['src']['scan']['colorMode'] = 'grayscale'
    payload['src']['scan']['contentType'] = 'photo'
    Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload)
    reset_payload()
    scan_emulation.media.unload_media('ADF')
    payload['src']['scan']['contentType'] = 'text'
    Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload)
    reset_payload()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Testing the copy quality options from the copy menu
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-34803
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_settings_quality
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_settings_quality
        +guid:d2582a31-53c7-4aa4-afa7-b822ef096271
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=CopyColor & FlatbedMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_settings_quality(cdm, udw):
    payload['dest']['print']['printQuality'] = 'draft'
    Copy(cdm, udw).do_copy_job(**payload)
    reset_payload()

    payload['dest']['print']['printQuality'] = 'best'
    Copy(cdm, udw).do_copy_job(**payload)
    reset_payload()
 
 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: duplex copy to simplex
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17184
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_duplex_simplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_duplex_simplex_using_cdm
        +guid:fb42172e-b18a-4007-9088-b801451b85a4
        +dut:
            +type: Simulator
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


def test_copy_duplex_simplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',6)
    payload1['src']['scan']['plexMode'] = 'duplex'
    payload1['dest']['print']['plexMode'] = 'simplex'
    Copy(cdm, udw).do_copy_job(**payload1)
    scan_emulation.media.unload_media('ADF')


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: duplex copy to duplex
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17184
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_duplex_duplex_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_duplex_duplex_using_cdm
        +guid:1b0489a8-7f7a-4a33-9422-06b1e9bd7276
        +dut:
            +type: Simulator
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


def test_copy_duplex_duplex_using_cdm(cdm, udw,scan_emulation):
    scan_emulation.media.load_media('ADF',6)
    payload['src']['scan']['plexMode'] = 'duplex'
    payload['dest']['print']['plexMode'] = 'duplex'
    Copy(cdm, udw).do_copy_job(**payload1)
    scan_emulation.media.load_media('ADF',1)
