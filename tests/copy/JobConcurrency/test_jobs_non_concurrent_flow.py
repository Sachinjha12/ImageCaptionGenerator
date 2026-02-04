import pytest
import time
from time import sleep
import logging
from dunetuf.job.job import Job
from dunetuf.copy.copy import *
from dunetuf.send.email.email import *
from dunetuf.addressBook.addressBook import *
from dunetuf.send.common import common
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.cdm import CDM
from dunetuf.udw import DuneUnderware
from tests.send.SendToEmail.EmailCommon import EmailTestUtils
from selenium.webdriver.common.by import By
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.send.usb import usb

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To check non concurrent copy job flow from copyapp
    +test_tier:2
    +is_manual:False
    +reqid:DUNE-95164
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_job_non_concurrent_flow
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_job_non_concurrent_flow
        +guid:2e5b1320-d296-4e8f-a529-356d85949374
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & JobHistory=SingleJob & JobType=NonConcurrent
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_job_non_concurrent_flow(spice, job, cdm, udw, net, configuration):
    # Steps is as follows:
    #   1. Move to copy and start the job
    #   2. Check for full screen UI and click on ok on completed screen
    try:
        job.bookmark_jobs()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.start_copy()
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net,configuration)
        okButton = spice.query_item(CopyAppWorkflowObjectIds.ok_button_constrained_message)
        okButton.mouse_click()
        copy_job_app.wait_for_copy_landing_view()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    finally:
        
        spice.goto_homescreen()
        spice.wait_ready()
