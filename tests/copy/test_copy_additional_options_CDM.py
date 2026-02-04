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
