import logging
from typing import Dict, List

import pytest
import time

from dunetuf.job.job import Job
from dunetuf.copy.copy import *


def get_ticket(cdm, ticket_id: str) -> Dict:
    rep = cdm.get_raw(cdm.JOB_TICKET_MODIFY_ENDPOINT.format(ticket_id))
    return rep.json()


def set_ticket(cdm, ticket_id: str, body: Dict):
    
    rep = cdm.patch_raw(cdm.JOB_TICKET_MODIFY_ENDPOINT.format(ticket_id), body)
    rep.raise_for_status()


def get_constraints(cdm, ticket_id: str) -> Dict:
    rep = cdm.get_raw(cdm.JOB_TICKET_CONSTRAINTS_ENDPOINT.format(ticket_id))
    rep.raise_for_status()
    return rep.json()['validators']


def enabled_options(validators: Dict, path: str) -> List[str]:
    prop = [x for x in validators if x['propertyPointer'] == path][0]
    enabled = [x['seValue'] for x in prop['options']
               if ('disabled' not in x) or x['disabled'] == 'false']
    logging.debug(f'{path}: enabled options: {enabled}')
    return enabled

def rotated_media_size_supported(tray):
    if tray.is_size_supported("com.hp.ext.mediaSize.na_letter_8.5x11in.rotated", 'tray-1'):
        return True
    else:
        return False
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verification of forcet application of Mixed Original Size
        1. Wait for home screen.
        2. Load ADF
        3. Load/configure Tray 1 with Plain Letter.
        4. Set input size to Mixed Letter-Legal.
        5. Start Copy job.
        6. Validate that cdm's inputmediasize is set to mixed letter-legal.
        7. Wait for jobs to complete, verify success.
        8. Unload ADF
        9. Start Copy job.
        10. Validating that cdm's inputmediasize is set to letter rotate by forceset.
        11. Wait for jobs to complete, verify success.
        12. Cleanup: Reset, to change Copy count.
        13. Cleanup: Reset trays.
        14. Cleanup: Clear ADF media.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106571
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_job_verify_forceset_application_of_Mixed_Original_Size
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_job_verify_forceset_application_of_Mixed_Original_Size
        +guid:e09363e2-ca01-451e-829c-d2db979fe3eb
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & ADFMediaSize=MixedLetterLegal & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_job_verify_forceset_application_of_Mixed_Original_Size(job, tray, cdm, device, udw, spice, configuration):
    try:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        udw.mainApp.ScanDeviceService.setNumScanPages(2)

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("MIXED_LETTER_LEGAL")
        spice.copy_ui().back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size= "com.hp.ext.mediaSize.mixed-letter-legal")
        time.sleep(7)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
        
        time.sleep(3)
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded = False)
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size= "na_letter_8.5x11in")
        time.sleep(5)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
        
        
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        udw.mainApp.ScanMedia.loadMedia("ADF")
        tray.reset_trays() 
