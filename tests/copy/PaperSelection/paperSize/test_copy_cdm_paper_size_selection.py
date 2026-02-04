import json
import time
import pytest
import requests
from dunetuf.copy.copy import *
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation, TrayLevel


#------------------------------------------------------------------------------
# Parse the command line arguments
#------------------------------------------------------------------------------

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", action="store_true", default=False, help="Print debug messages to stdout")
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Print info messages to stdout")
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

    # Mixed letter legal is not supported for print media size in Copy, configure tray with Letter
    supported_print_media_sizes = get_supported_print_media_sizes(cdm)
    new_media_size = media_size if media_size in supported_print_media_sizes else "na_letter_8.5x11in"
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
        cdm.alerts.wait_for_alerts('sizeType', 5)
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
        cdm.alerts.wait_for_alerts('sizeType', 5)
        media.alert_action(category='sizeType', response='ok')
    except:
        logging.debug("SizeType Alert does not appear")

# Scan supported Original Size (ADF and FB)
def get_scan_supported_media_sizes(cdm):
    copy_constraints = cdm.get_raw(cdm.JOB_TICKET_COPY_CONSTRAINTS).json()
    supported_scan_media_sizes = []
    for constraint in copy_constraints["validators"]:
        if constraint["propertyPointer"] == "src/scan/mediaSize":
            for value in constraint.get("options"):
                supported_scan_media_sizes.append(value["seValue"])
                if "disabled" in value and value["disabled"] == "true":
                    supported_scan_media_sizes.remove(value["seValue"])
    return supported_scan_media_sizes

# Supported print media size
def get_supported_print_media_sizes(cdm):
    copy_constraints = cdm.get_raw(cdm.JOB_TICKET_COPY_CONSTRAINTS).json()
    supported_print_media_sizes = []
    for constraint in copy_constraints["validators"]:
        if constraint["propertyPointer"] == "dest/print/mediaSize":
            for value in constraint.get("options"):
                supported_print_media_sizes.append(value["seValue"])
                if "disabled" in value and value["disabled"] == "true":
                    supported_print_media_sizes.remove(value["seValue"])
    return supported_print_media_sizes
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using the Legal paper size
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17187
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_paper_legal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_paper_legal
        +guid:195fab67-1909-4c61-a72c-4e154c241f52
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Legal & ScanColorMode=Automatic
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_paper_legal(cdm, udw, media, scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    original_data = scan_status_cdm_trayconfig(cdm, media, 1, "na_legal_8.5x14in", "stationery")
    payload['src']['scan']['mediaSize'] = 'na_legal_8.5x14in'
    payload['dest']['print']['mediaSize'] = 'na_legal_8.5x14in'
    payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
    scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using the A5 paper size
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17187
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_paper_a5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_cdm_paper_a5
        +guid:48f9c997-43ed-4530-b462-68fd3b1f5750
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A5
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_paper_a5(cdm, udw, media, scan_emulation):
    scan_emulation.media.load_media('ADF',1)
    original_data = scan_status_cdm_trayconfig(cdm, media, 1, "iso_a5_148x210mm", "stationery")
    payload['src']['scan']['mediaSize'] = 'iso_a5_148x210mm'
    payload['dest']['print']['mediaSize'] = 'iso_a5_148x210mm'
    payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
    scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test plain paper copy jobs using all paper sizes
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-45557
    +timeout:900
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_plain_paper_all_sizes
    +test:
        +title:test_copy_cdm_plain_paper_all_sizes
        +guid:ae7fd8c2-b4d8-4adf-b8b2-4b710e7bffe7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaType=Plain
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_cdm_plain_paper_all_sizes(cdm, udw, media, scan_emulation):
    supported_scan_media_sizes = get_scan_supported_media_sizes(cdm)
    logging.debug("Scan supported media sizes :: {0}".format(supported_scan_media_sizes))

    supported_print_media_sizes = get_supported_print_media_sizes(cdm)
    logging.debug("Print supported media sizes :: {0}".format(supported_print_media_sizes))

    # Iterate supported media sizes
    for supported_size in supported_scan_media_sizes:
        # Unload media from flatbed
        scan_emulation.media.unload_media('Flatbed')

        # Load media in ADF and set tray
        # Load 2 pages in ADF for mixed paper sizes
        if supported_size in ["com.hp.ext.mediaSize.mixed-letter-legal","com.hp.ext.mediaSize.mixed-letter-ledger","com.hp.ext.mediaSize.mixed-a4-a3"]:
            scan_emulation.media.load_media('ADF', 2)
        else:
            scan_emulation.media.load_media('ADF', 1)
        original_data = scan_status_cdm_trayconfig(cdm, media, 1, supported_size, "stationery")

        # Create Copy Job payload
        payload['src']['scan']['mediaSource'] = 'adf'
        payload['src']['scan']['mediaSize'] = supported_size
        # If the print media size is mixed-letter-legal, set the media size to letter
        payload['dest']['print']['mediaSize'] = supported_size if supported_size in supported_print_media_sizes else "na_letter_8.5x11in"
        payload['dest']['print']['mediaType'] = 'stationery'
        # For mixed paper sizes, set the media source to auto
        if supported_size in ["com.hp.ext.mediaSize.mixed-letter-legal","com.hp.ext.mediaSize.mixed-letter-ledger","com.hp.ext.mediaSize.mixed-a4-a3"]:
            payload['dest']['print']['mediaSource'] = "auto"
        else:
            payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']

        # Perform Copy Job
        Copy(cdm, udw).do_copy_job(**payload)

        # Cleanup tray setting and unload media
        scan_emulation.media.unload_media('ADF')
        scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test light paper copy jobs using all paper sizes
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-45557
    +timeout:600
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_cdm_light_paper_all_sizes
    +test:
        +title:test_copy_cdm_light_paper_all_sizes
        +guid:5d08cf86-9577-4766-9226-f5c9a46dca7d
        +dut:
            +type:Simulator
            +configuration:DoXSupported=True & PrintEngineType=Canon & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaType=Plain
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_cdm_light_paper_all_sizes(cdm, udw, media, scan_emulation):
    supported_scan_media_sizes = get_scan_supported_media_sizes(cdm)
    logging.debug("Scan supported media sizes :: {0}".format(supported_scan_media_sizes))

    # Iterate supported media sizes
    for supported_size in supported_scan_media_sizes:
        # Load media in ADF and set tray
        scan_emulation.media.load_media('ADF',1)
        original_data = scan_status_cdm_trayconfig(cdm, media, 1, supported_size, "stationery-lightweight")

        # Create Copy Job payload
        payload['src']['scan']['mediaSource'] = 'adf'
        payload['src']['scan']['mediaSize'] = supported_size
        payload['dest']['print']['mediaSize'] = supported_size
        payload['dest']['print']['mediaType'] = 'stationery-lightweight'
        payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']

        # Perform Copy Job
        Copy(cdm, udw).do_copy_job(**payload)

        # Cleanup tray setting and unload media
        scan_emulation.media.unload_media('ADF')
        scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test recycled paper copy jobs using all paper sizes
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-45557
    +timeout:600
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_cdm_recycled_paper_all_sizes
    +test:
        +title:test_copy_cdm_recycled_paper_all_sizes
        +guid:d191c9f9-6051-4a25-9722-4ef766ff7261
        +dut:
            +type:Simulator
            +configuration:DoXSupported=True & PrintEngineType=Canon & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaType=Recycled
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_cdm_recycled_paper_all_sizes(cdm, udw, media, scan_emulation):
    supported_scan_media_sizes = get_scan_supported_media_sizes(cdm)
    logging.debug("Scan supported media sizes :: {0}".format(supported_scan_media_sizes))

    # Iterate supported media sizes
    for supported_size in supported_scan_media_sizes:
        # Load media in ADF and set tray
        scan_emulation.media.load_media('ADF',1)
        original_data = scan_status_cdm_trayconfig(cdm, media, 1, supported_size, "com.hp.recycled")

        # Create Copy Job payload
        payload['src']['scan']['mediaSource'] = 'adf'
        payload['src']['scan']['mediaSize'] = supported_size
        payload['dest']['print']['mediaSize'] = supported_size
        payload['dest']['print']['mediaType'] = 'com.hp.recycled'
        payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']

        # Perform Copy Job
        Copy(cdm, udw).do_copy_job(**payload)

        # Cleanup tray setting and unload media
        scan_emulation.media.unload_media('ADF')
        scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test photo paper matte and glossy copy jobs using A4 paper size
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-45557
    +timeout:600
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_cdm_photo_paper_A4
    +test:
        +title:test_copy_cdm_photo_paper_A4
        +guid:1786111d-0668-4969-b0c7-a88cf4f70a1f
        +dut:
            +type:Simulator
            +configuration:DoXSupported=True & PrintEngineType=Canon & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_cdm_photo_paper_A4(cdm, udw, media,scan_emulation, tray):
    photo_paper_media_types = { "com.hp.matte-90gsm", "com.hp.matte-105gsm","com.hp.matte-120gsm", "com.hp.glossy-220gsm",
                               "com.hp.matte-200gsm", "com.hp.glossy-130gsm", "com.hp.glossy-160gsm", "com.hp.cardstock-glossy",
                               "com.hp.heavy-glossy", "com.hp.extra-heavy-gloss",  "stationery-letterhead",
                               "com.hp-photographic-inkjet", "stationery-heavyweight",}

    support_type_list = tray.get_supported_types("tray-1")
    support_photo_paper_media_types = [media_type for media_type in support_type_list if media_type in photo_paper_media_types]
    assert len(support_photo_paper_media_types) > 0, f"device not support photo_paper_media_types: {photo_paper_media_types}"
    logging.debug("support_photo_paper_media_types ::{0}".format(support_photo_paper_media_types))

    # Iterate all matte media types and perform copy job with aA4 size/media type combination
    for mediatype in support_photo_paper_media_types:
        logging.debug("Testing paper type : {0}".format(mediatype))
        # Load media in ADF and set tray
        scan_emulation.media.load_media('ADF',1)
        original_data = scan_status_cdm_trayconfig(cdm, media, 1, "iso_a4_210x297mm", mediatype)

        # Create Copy Job payload
        payload['src']['scan']['mediaSource'] = 'adf'
        payload['src']['scan']['mediaSize'] = "iso_a4_210x297mm"
        payload['dest']['print']['mediaSize'] ="iso_a4_210x297mm"
        payload['dest']['print']['mediaType'] = mediatype
        payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']

        # Perform Copy Job
        Copy(cdm, udw).do_copy_job(**payload)

        # Cleanup tray setting and unload media
        scan_emulation.media.unload_media('ADF')
        scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)


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
    +name: test_copy_cdm_paper_letter
    +test:
        +title: test_copy_cdm_paper_letter
        +guid:37b5e6b5-14f1-41fc-b0c8-2e6ba303ea46
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
        +ProA4:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_paper_letter(cdm, udw, media, scan_emulation, print_emulation):
    scan_emulation.media.load_media('ADF',1)
    tray1= MediaInputIds.Tray1.name
    print_emulation.tray.empty(tray1)
    print_emulation.tray.load(tray1, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name, status_values='READY, OCCUPIED')
    original_data = scan_status_cdm_trayconfig(cdm, media, 1, "na_letter_8.5x11in", "stationery")
    payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
    scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)
    print_emulation.tray.reset_trays()
    scan_emulation.media.load_media('ADF',1)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test copy jobs using the A4 paper size
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-17187
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy__a4_using_cdm
    +test:
        +title: test_copy__a4_using_cdm
        +guid:717dc1b6-c4c0-461d-b295-4032dff53ec0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4
    +overrides:
        +ProA4:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy__a4_using_cdm(cdm, udw, media, scan_emulation, print_emulation):
    scan_emulation.media.load_media('ADF',1)
    tray1= MediaInputIds.Tray1.name
    print_emulation.tray.empty(tray1)
    print_emulation.tray.load(tray1, MediaSize.A4.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name, status_values='READY, OCCUPIED')
    original_data = scan_status_cdm_trayconfig(cdm, media, 1, "iso_a4_210x297mm", "stationery")
    payload['src']['scan']['mediaSize'] = 'iso_a4_210x297mm'
    payload['dest']['print']['mediaSize'] = 'iso_a4_210x297mm'
    # Get tray from cdm as the default tray is different for different machines.
    payload['dest']['print']['mediaSource'] = original_data['mediaSourceId']
    Copy(cdm, udw).do_copy_job(**payload)
    scan_emulation.media.unload_media('ADF')
    scan_status_cdm_trayconfig_reset(cdm, media, 1, original_data)

    # Reset the trays to their default size and type
    print_emulation.tray.reset_trays()
