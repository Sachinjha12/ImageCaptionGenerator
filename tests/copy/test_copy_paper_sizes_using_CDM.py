from select import select
from dunetuf.copy.copy import *
from dunetuf.metadata import get_metadata, set_metadata
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
import requests
import json
import time

import pytest

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
                    'colorMode':'Automatic',
                    'mediaSize':'na_letter_8.5x11in',
                    'plexMode':'simplex',
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

#------------------------------------------------------------------------------
# Endpoint for Tray config
#------------------------------------------------------------------------------


#-------------------------------------------------------------------------------------
# mediaSize dictionary to map the media size from metadata to actual media size string
#-------------------------------------------------------------------------------------
mediaSize_dict = {"ScanA4" : "iso_a4_210x297mm", "ScanA5": "iso_a5_148x210mm", "ScanA6": "iso_a6_105x148mm",
                     "ScanB5Envelope" : "iso_b5_176x250mm", "ScanC5Envelope" : "iso_c5_162x229mm",
                     "ScanCOM10Envelope": "na_number-10_4.125x9.5in", "ScanJDoublePostcard" : "jpn_oufuku_148x200mm",
                     "ScanDLEnvelope" : "iso_dl_110x220mm", "ScanExecutive" : "na_executive_7.25x10.5in", 
                     "ScanFiveXEight" : "na_index-5x8_5x8in", "ScanLetter" : "na_letter_8.5x11in", 
                     "Scan4XSix" : "na_index-4x6_4x6in", "ScanLegal" : "na_legal_8.5x14in", 
                     "ScanJisB5" : "jis_b5_182x257mm" , "ScanJisB6" : "jis_b6_128x182mm",
                     "ScanSixteenK" : "roc_16k_7.75x10.75in", "ScanSize16K184x260" : "om_16k_184x260mm",
                     "ScanSize16k195x270": "om_16k_195x270mm", "ScanStatement" : "na_invoice_5.5x8.5in",
                     }

#------------------------------------------------------------------------------
# cdm_trayconfig_patch_helper
#------------------------------------------------------------------------------

def cdm_trayconfig_patch_helper(cdm, endpoint, payload, test_name):
    try:
        response = cdm.patch_raw(endpoint, payload)
        log.info(f"{test_name} PATCH:1 Route: {endpoint} Payload: {payload} Response: {response}")
        assert response != 0
        return response
    except Exception as e:
        assert False, f"{test_name} Failed to PATCH {endpoint} exception = {e}"

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
# cdm_trayconfig_configuration_patch_valid_payload
#------------------------------------------------------------------------------

# Test PATCH operation for configuration route
def scan_status_cdm_trayconfig(cdm, media, tray, media_size, media_type):
    # GET tray configuration data from printer
    response = cdm_trayconfig_get_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, "scan_status_cdm_trayconfig:GET:1")
    assert response['inputs'][tray - 1] != 0

    # Saving to return printer to default state
    original_data = response['inputs'][tray - 1]

    # Setup test data
    media_id = response['inputs'][tray - 1]['mediaSourceId']
    
    new_media_size = media_size
    new_media_type = media_type

    # Valid tray input
    test_data = {
        "mediaSourceId" : media_id,
        "currentMediaSize" : new_media_size,
        "currentMediaType" : new_media_type
    }

    # Valid PATCH payload with test_data
    patch_body = {
        "version": "0.1.0",
        "inputs": [test_data],
        "outputs" : [],
    }

    # Send the payload
    response = cdm_trayconfig_patch_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, patch_body, "scan_status_cdm_trayconfig:PATCH:1")
    assert response.status_code == 204

    # Get modified data and verify
    response = cdm_trayconfig_get_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, "scan_status_cdm_trayconfig:GET:2")
    assert response['inputs'][tray - 1] != test_data

    try:
        cdm.alerts.wait_for_alerts('sizeType')
        media.alert_action(category='sizeType', response='ok')
    except:
        logging.debug("SizeType Alert does not appear")

    return original_data

def scan_status_cdm_trayconfig_reset(cdm, media, tray, original_data):
    # Valid PATCH payload original_data 
    patch_body = {
        "version": "0.1.0",
        "inputs": [original_data],
        "outputs" : [],
    }

    # Revert changes
    response = cdm_trayconfig_patch_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, patch_body, "scan_status_cdm_trayconfig_reset:PATCH:1")
    assert response.status_code == 204

    # Get reverted data and verify
    response = cdm_trayconfig_get_helper(cdm, cdm.CDM_MEDIA_CONFIGURATION, "scan_status_cdm_trayconfig_reset:GET:1")
    assert response['inputs'][tray - 1] == original_data

    try:
        cdm.alerts.wait_for_alerts('sizeType',5)
        media.alert_action(category='sizeType', response='ok')
    except:
        logging.debug("SizeType Alert does not appear")

def get_product_metadata(configuration):
 
    # URL for fetching SKU metadata
    # https://dune-btf-ui.boi.rd.hpicorp.net/webservices/v1/getSKUMetaData?SKUName=selene-linux-x86_32-debug&productName=Selene"

    # dictionary to store the skun_name corresponding to product under Test
    # This mapping should be revisited and updated once the SKU names in metdata site is fixed  
    skudict = {
        "selene" : "HP Color LaserJet Pro MFP M481 (4RA80A) [DW]",
        "marconihi" : "Marconi Hi",
        "jasper" : "hpmfp",
        "eddington" : "Eddington",
        "moretohi" : "MoretoHi",
        "camden" : "HP Color LaserJet Managed MFP E47528f"
    }
    
    sku_product = configuration.productname
    sku_product = sku_product.split("/")[1] if "/" in sku_product else sku_product
    sku_name = skudict[sku_product]
    if sku_product == 'eddington':
        sku_product = "Kebin"

    if sku_product == 'moretohi':
        sku_product = 'moreto'

    if sku_product == 'camden':
	    sku_product = 'canonmfp'

    try:
        url = (
            "https://dune-btf-ui.boi.rd.hpicorp.net/webservices/v1/getSKUMetaData?"
            "SKUName={}&productName={}"
        )
        # TODO: Remove this verify=False to enable SSL verification once this server is
        # configured with the HP Root certificate
        if sku_product == "jasper":
            sku_md_response = requests.get(
                url.format(sku_product, sku_name), verify=False
            )
        else:
            sku_md_response = requests.get(
                url.format(sku_name, sku_product), verify=False
            )

        sku_md_dict = json.loads(sku_md_response.text)

        # Call set_metadata
        set_metadata(sku_md_dict)

        metadata_dict = get_metadata()

        return metadata_dict

    except:
        raise Exception("Error in fetching SKU metadata from URL " + url)    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using the letter paper size
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17187
    +timeout:180
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_letter_using_cdm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_letter_using_cdm
        +guid:0baad69c-d60c-4e8d-b3f0-8bbda90c0ff9
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_letter_using_cdm(cdm, udw, media, scan_emulation, print_emulation):
    scan_emulation.media.load_media('ADF',1)
    tray1= MediaInputIds.Tray1.name
    print_emulation.tray.empty(tray1)
    print_emulation.tray.load(tray1, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name, status_values='READY, OCCUPIED')
    original_data = scan_status_cdm_trayconfig(cdm, media, 1, "na_letter_8.5x11in", "stationery")
    payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
    scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)
    scan_emulation.media.load_media('ADF',1)
    print_emulation.tray.reset_trays()





        
        
