from dunetuf.copy.copy import *
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel

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





#------------------------------------------------------------------------------
# cdm_trayconfig_get_helper
#------------------------------------------------------------------------------

def cdm_trayconfig_get_helper(cdm, endpoint, test_name):
    try:
        response = cdm.get(endpoint)
        log.info(f"{test_name} Route: {endpoint} Response: {response}")
        assert response != 0
        return response
    except Exception as e:
        assert False, f"{test_name} Failed to GET {endpoint} exception = {e}"

#------------------------------------------------------------------------------
# cdm_trayconfig_configuration_get
#------------------------------------------------------------------------------

payload = {
            'src': {
                'scan': {
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
                },
            },
            'dest': {
                'print': {
                    'copies': 1,
                    'mediaSource': 'auto',
                    'mediaSize':'na_letter_8.5x11in',
                    'mediaType': 'stationery',
                    'plexMode':'simplex',
                }
            }
        }

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: single page copy from flatbed where all the supported trays
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17188
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_trays_all_supported_flatbed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_trays_all_supported_flatbed
        +guid:43c25451-9eef-4984-b9fd-e22a2f632c4a
        +dut:
            +type: Simulator 
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

def test_copy_trays_all_supported_flatbed(cdm,scan_emulation, print_emulation, tray, udw, media):
    try:
        tray_mapping = {
            'tray-1': MediaInputIds.Tray1.name,
            'tray-2': MediaInputIds.Tray2.name,
            'tray-3': MediaInputIds.Tray3.name,
            'tray-4': MediaInputIds.Tray4.name,
            'tray-5': MediaInputIds.Tray5.name,
            'tray-6': MediaInputIds.Tray6.name
        }
        
        scan_emulation.media.unload_media('ADF')
        
        # GET tray configuration data from printer
        response = cdm_trayconfig_get_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, "cdm_trayconfig_configuration_patch_valid_payload:GET:1")
        assert response['inputs'] != 0

        # Saving to return printer to default state
        original_data = response['inputs']

        for input_media_source in original_data:
            # Get media source and Save to job ticket.
            payload['dest']['print']['mediaSource'] = input_media_source['mediaSourceId']
            payload['dest']['print']['mediaSize'] = input_media_source['currentMediaSize']
            payload['dest']['print']['mediaType'] = input_media_source['currentMediaType']
            # Change Media size and media type to Letter and Plain if Tray default Size and type is any,any.
            if (input_media_source['currentMediaSize'] == "any"):
                Tray = input_media_source['mediaSourceId']
                trayId = tray_mapping.get(Tray)
                print_emulation.tray.empty(trayId)
                print_emulation.tray.load(trayId, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
                tray.configure_tray(Tray, 'na_letter_8.5x11in', 'stationery')
                try:
                    cdm.alerts.wait_for_alerts('sizeType', 3)
                    media.alert_action(category='sizeType', response='ok')
                except:
                    logging.info("sizeType alert not found")
                payload['dest']['print']['mediaSize'] = 'na_letter_8.5x11in'
                payload['dest']['print']['mediaType'] = 'stationery'
            Copy(cdm, udw).do_copy_job(**payload, waitTime=90)
    finally:
        scan_emulation.media.load_media('ADF')
        print_emulation.tray.reset_trays()