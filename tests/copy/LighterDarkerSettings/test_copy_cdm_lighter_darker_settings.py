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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Testing the lighter/darker options from the copy menu
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-34797
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_lighter_darker
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_lighter_darker
        +guid:4bdc8ea8-71ca-48e6-b92c-b012227207e5
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & FlatbedMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator    
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_lighter_darker(cdm, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    payload['pipelineOptions']['imageModifications']['exposure'] = 9
    Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload)
    reset_payload()
    scan_emulation.media.unload_media('ADF')
    payload['pipelineOptions']['imageModifications']['exposure'] = 2
    Copy(cdm, udw).do_copy_job(adfLoaded = False, **payload)
    reset_payload()
    scan_emulation.media.load_media('ADF')
