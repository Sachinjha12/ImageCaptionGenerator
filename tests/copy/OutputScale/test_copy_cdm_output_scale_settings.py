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
    +purpose: Testing the scale percent options from the copy menu
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17186
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_scale_percent
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_scale_percent
        +guid:25f411d1-592c-457d-850a-68ee1fb9651c
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & FlatbedMediaSize=Letter
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_scale_percent(cdm, udw):

    payload['pipelineOptions']['scaling']['xScalePercent'] = 50
    payload['pipelineOptions']['scaling']['yScalePercent'] = 50
    Copy(cdm, udw).do_copy_job(**payload)
    reset_payload()

    payload['pipelineOptions']['scaling']['xScalePercent'] = 200
    payload['pipelineOptions']['scaling']['yScalePercent'] = 200
    Copy(cdm, udw).do_copy_job(**payload)
    reset_payload()
