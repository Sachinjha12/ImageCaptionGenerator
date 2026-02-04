import json
import time
import pytest
import requests
from dunetuf.copy.copy import *
from dunetuf.print.print_common_types import MediaInputIds, MediaSize, MediaType, MediaOrientation, TrayLevel
from dunetuf.job.job import Job

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
        cdm.alerts.wait_for_alerts('sizeType', 5)
        media.alert_action(category='sizeType', response='ok')
    except:
        logging.debug("SizeType Alert does not appear")

    return original_data

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


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: This test is a Scan Ahead test. After the scan is completed after starting the copy, the copy button is activated and a new copy is performed, verifying that the first and second copy jobs are completed normally.
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-221701
    +timeout:900
    +asset: Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework: TUF
    +name: test_copy_scan_ahead_and_copy_complete_verify
    +test:
        +title: test_copy_scan_ahead_and_copy_complete_verify
        +guid:3769d06f-b016-4fc8-966b-5ee9d8c4cb2f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:900
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_scan_ahead_and_copy_complete_verify(cdm, spice, job, udw, media, scan_emulation, print_emulation):
    copy_job_app = spice.copy_ui()
    job.bookmark_jobs()

    try:
        #For the first scan, load 20 sheets into the ADF and set Tray1.
        scan_emulation.media.load_media('ADF', 20)
        tray1= MediaInputIds.Tray1.name
        print_emulation.tray.empty(tray1)
        print_emulation.tray.load(tray1, MediaSize.A4.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name, status_values='READY, OCCUPIED')
        scan_status_cdm_trayconfig(cdm, media, 1, "iso_a4_210x297mm", "stationery")  
        
        job_ids = job.get_recent_job_ids()
        first_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        #First copy start
        copy_job_app.goto_copy()
        copy_job_app.change_num_copyApp_copies(2)
        copy_job_app.goto_copy_options_list()
        copy_job_app.change_collate(collate_option="off")
        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        #Check scanner working
        Copy(cdm, udw).wait_for_corresponding_scanner_status_with_cdm("Processing")
        copy_job_app.validate_copy_and_scan_in_progress(scan_progress=True)   

        #Wait until scan is complete and printing begins
        Copy(cdm, udw).wait_for_corresponding_scanner_status_with_cdm("Idle")
        job.wait_for_job_state(first_job_id, state="READY")
        copy_job_app.validate_copy_and_scan_in_progress(scan_progress=False)

        #For the second scan, load 15 sheets into the ADF and set Tray1.
        scan_emulation.media.load_media('ADF', 15)

        #Check Second jobId
        job_ids = job.get_recent_job_ids()
        second_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        #Second copy start
        copy_job_app.start_copy()

        # Verify that the first copy job is complete
        first_copy_job_id = Job.wait_for_completed_job(first_job_id, job, udw, total_time = 200)
        Job.verify_job_status_udw(udw, first_copy_job_id, "COMPLETED", "SUCCESS")
        
        # Verify that the second copy job is complete and the impression count
        second_copy_job_id = Job.wait_for_completed_job(second_job_id, job, udw, total_time = 200)
        Job.verify_job_status_udw(udw, second_copy_job_id, "COMPLETED", "SUCCESS")
        
        job_ids = job.get_newjobs()
        first_copy_job_id_cdm = job_ids[len(job_ids) - 2]['jobId']
        second_copy_job_id_cdm = job_ids[len(job_ids) - 1]['jobId']
        
        # Verify that the first copy job impression count
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + first_copy_job_id_cdm)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        assert cdm_response['printInfo']['impressionCount'] == 40 , "Number of printed pages mismatch"

        # Verify that the second copy job impression count
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + second_copy_job_id_cdm)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        assert cdm_response['printInfo']['impressionCount'] == 30 , "Number of printed pages mismatch"
        
    finally:
        scan_emulation.media.unload_media('ADF')
        logging.info("back to the home screen")
        spice.goto_homescreen()
        # Reset the trays to their default size and type
        print_emulation.tray.reset_trays()