import os
import time
import logging
import json
import pytest
import sys
import logging

from dunetuf.power.power import Power
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.ssh import SSH
from tests.copy.Contention.contention_common import send_print_job_from_usb, execute_print_storejob, execute_ipp_print_job, dismiss_load_paper_alert
from dunetuf.send.jobStorage import jobStorage
from dunetuf.send.common import common
from dunetuf.copy.copy import Copy
from dunetuf.power.power import *
from dunetuf.print.output.intents import Intents
from dunetuf.send.folder.folder import *
from dunetuf.copy.copy import Cancel as CopyCancel
from dunetuf.send.common.common import Cancel as CommonCancel
from dunetuf.cdm.CdmEndpoints import CdmEndpoints
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.copy import copy

def create_stored_job(spice, job):
    # create a stored job
    job_name = "Job1"
    spice.scan_job_storage.goto_send_to_job_storage_from_admin_app()
    spice.scan_job_storage.input_job_name_in_landing_view(job_name)
    spice.scan_job_storage.press_save_to_job_storage()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    spice.goto_homescreen()  

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Create the store job and retrieve with default settings
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-193674
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_stored_job_retrive
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_cdm_stored_job_retrive
        +guid:f9c83273-20d4-4a55-8b8e-a9ed6c8df516
        +dut: 
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanDestination=JobStorage
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
 
def test_copy_cdm_stored_job_retrive(spice, cdm, udw, job, media, configuration, dunestorejob):
   
    # step 1 - create a stored job 
    create_stored_job(spice, job)
    
    # step 2 - get the stored folder link and check the stored jobs available
    storejobs = dunestorejob.get_all()    
    assert len(storejobs) >= 1, 'Unexpected number of stored jobs found!'
    storejob = storejobs[0]
    storejob_folder_id = storejob['folderId']
    response = cdm.get_raw(cdm.FOLDER_JOBS_ENDPOINT.format(storejob_folder_id))
    storejob1 = json.loads(response.text)
    
    logging.info("response ",response.json())
    # step 3 - Extract href from the stored job link
    job_href = next(link['href'] for link in storejob1['jobs'][0]['links'] if link['rel'] == 'self')
    logging.info("href = ", job_href)

    # step 4 - ticket from the stored job ref
    payload = {
        'ticketReference': CdmEndpoints.JOB_TICKET_CONFIGURATION_DEFAULT_COPY,
        'replayJobReference': job_href 
    }

    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, payload)
    assert ticket_user_response.status_code == 201

    ticket_user_body = ticket_user_response.json()
    # get ticket id
    ticket_id = ticket_user_body["ticketId"]
    logging.info("ticket_id = ", ticket_id)
    
    payload = {'ticketId': ticket_id, 'autoStart': True}
    response = cdm.post_raw(cdm.JOB_MANAGEMENT_JOBS_END_POINT, payload)

    logging.info("job response ", response.status_code)
    assert response.status_code == 201
    response1 = response.json()
    job_info_url = job.get_current_job_url("copy")
    #Wait for copy job to completed else Scanned Pages from ADF will change
    job.wait_for_job_state_complete_successfully(job_info_url,time_out=30)
    
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Create the store job and retrieve with copies changed to 2
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-193674
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_cdm_stored_job_retrive_two_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test: 
        +title: test_copy_cdm_stored_job_retrive_two_copies
        +guid:e6932650-8892-47f2-b344-4808e4a57136
        +dut: 
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanDestination=JobStorage
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_cdm_stored_job_retrive_two_copies(spice, cdm, udw, job, media, configuration, dunestorejob):
   
    # step 1 - create a stored job 
    create_stored_job(spice, job)
    
    # step 2 - get the stored folder link and check the stored jobs available
    storejobs = dunestorejob.get_all()    
    assert len(storejobs) >= 1, 'Unexpected number of stored jobs found!'
    storejob = storejobs[0]
    storejob_folder_id = storejob['folderId']
    response = cdm.get_raw(cdm.FOLDER_JOBS_ENDPOINT.format(storejob_folder_id))
    storejob1 = json.loads(response.text)
    
    logging.info("response ",response.json())
    # step 3 - Extract href from the stored job link
    job_href = next(link['href'] for link in storejob1['jobs'][0]['links'] if link['rel'] == 'self')
    logging.info("href = ", job_href)

    # step 4 - ticket from the stored job ref
    payload = {
        'ticketReference': CdmEndpoints.JOB_TICKET_CONFIGURATION_DEFAULT_COPY,
        'replayJobReference': job_href 
    }

    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, payload)
    assert ticket_user_response.status_code == 201

    ticket_user_body = ticket_user_response.json()
    # get ticket id
    ticket_id = ticket_user_body["ticketId"]
    ticket_info = job.get_job_ticket_info(ticket_id)
    logging.info("ticket_info = ", ticket_info)

    # step 5 - update the ticket with number of copies
    ticket_update = {
        "dest": {
            "print": {
                "copies": "2"
            }
        }
    }
    job.update_job_ticket(ticket_id, ticket_update)

    ticket_info = job.get_job_ticket_info(ticket_id)
    logging.info("updated ticket_info = ", ticket_info)

    payload = {'ticketId': ticket_id, 'autoStart': True}
    response = cdm.post_raw(cdm.JOB_MANAGEMENT_JOBS_END_POINT, payload)

    logging.info("job response ", response.status_code)
    assert response.status_code == 201
    
    logging.info(response.json())
    job_info_url = job.get_current_job_url("copy")
    job.wait_for_job_state_complete_successfully(job_info_url,time_out=30)
