import logging
from selenium.webdriver.common.by import By
from dunetuf.copy.copy import *
from random import randint
from tests.copy.ews.copy_default_settings.copy_ews_combination import *
from tests.copy.copy_ui_job import CopyReprintHelper
from dunetuf.ews.EwsCapabilities import EwsCapability

NUMBER_OF_COPIES_SELECTOR_LOCATOR = By.ID, "numberOfCopies"
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify reprinting the copy job works fine
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-119831
    +timeout:200
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_validate_successful_copy_jobs_are_reprintable
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Reprint
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_validate_successful_copy_jobs_are_reprintable
        +guid:10e67e3f-ce20-41c0-acec-335c2db3b784
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP &  DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_validate_successful_copy_jobs_are_reprintable(ews ,udw ,cdm ,net ,spice ,job ,configuration):
    if ews.is_supported(EwsCapability.FAMILY_DESIGNJET_LATEX):
        logging.info("This test if not valid for Sunspot as it does not support EWS Job Queue")
        return
    # clear the job history so we have a clean slate
    try:
        udw.mainApp.execute('JobHistory PUB_clearJobHistory')
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job ,net,configuration)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        spice.goto_homescreen()
        ews.load("jobs/jobQueue")
        ews.helper.wait_for_element_visible((By.XPATH, f"//mat-list-option[contains(@id,'{job_id}')]")).click()
        ews.helper.wait_for_then_click('cReprint')
        ews.helper.wait_for_then_click('footer-reprint-job-button-apply')
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        # Get job
        queue = job.get_job_history()
        job_id = queue[-1]["jobId"]
        assert len(queue)>0 ,"I can't get printed job"

        ews.helper.wait_for_element_visible((By.XPATH, f"//mat-list-option[contains(@id , '{job_id}')]"))
    finally:
        spice.goto_homescreen()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-119831
    +timeout:200
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_validate_cancelled_job_cannot_reprint
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Reprint
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_validate_cancelled_job_cannot_reprint
        +guid:7a5eac78-7b58-47b5-9987-1247d48d0d6b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_validate_cancelled_job_cannot_reprint(ews ,udw ,cdm ,net ,spice ,job ,configuration):
    if ews.is_supported(EwsCapability.FAMILY_DESIGNJET_LATEX):
        logging.info("This test if not valid for Sunspot as it does not support EWS Job Queue")
        return
    #clear the job history so we have a clean slate
    try:
        udw.mainApp.execute('JobHistory PUB_clearJobHistory')
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job ,net,configuration)
        job.cancel_job(job_id)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration,message = "Cancel")
        spice.goto_homescreen()

        ews.load("jobs/jobQueue")
        ews.helper.wait_for_element_visible((By.XPATH, f"//mat-list-option[contains(@id,'{job_id}')]")).click() 
        found = False  
        try:
            ews.helper.wait_for_element_visible(By.ID, 'cReprint')
            found =True
        except: pass
        assert not found
    finally:
        spice.goto_homescreen()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify reprinting the copy job works fine
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-119831
    +timeout:200
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_validate_no_copies_variable_btwn_min_max_from_reprint_window
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Reprint
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_validate_no_copies_variable_btwn_min_max_from_reprint_window
        +guid:f6e939ef-419a-4cf4-9da9-da3c994fce6c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & JobSettings=ReprintJob
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_validate_no_copies_variable_btwn_min_max_from_reprint_window(ews ,udw ,cdm ,net ,spice ,job ,configuration):
    if ews.is_supported(EwsCapability.FAMILY_DESIGNJET_LATEX):
        logging.info("This test if not valid for Sunspot as it does not support EWS Job Queue")
        return
    # clear the job history so we have a clean slate
    try:
        udw.mainApp.execute('JobHistory PUB_clearJobHistory')
        job_id = CopyReprintHelper.perform_copy_job(spice, cdm, udw, job ,net,configuration)
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration)
        spice.goto_homescreen()
        ews.load("jobs/jobQueue")
        ews.helper.wait_for_element_visible((By.XPATH, f"//mat-list-option[contains(@id,'{job_id}')]")).click()
        ews.helper.wait_for_then_click('cReprint')

        # check no of copies can be set btwn min to max
        random_no_copies = randint(CopyReprintHelper.min_no_copies, CopyReprintHelper.max_no_copies)
        ews.helper.wait_for_then_set_text(random_no_copies, NUMBER_OF_COPIES_SELECTOR_LOCATOR)
        random_no_copies = randint(CopyReprintHelper.min_no_copies, CopyReprintHelper.max_no_copies)
        ews.helper.wait_for_then_set_text(random_no_copies, NUMBER_OF_COPIES_SELECTOR_LOCATOR)
        random_no_copies = randint(CopyReprintHelper.min_no_copies, CopyReprintHelper.max_no_copies)
        ews.helper.wait_for_then_set_text(random_no_copies, NUMBER_OF_COPIES_SELECTOR_LOCATOR)
        
        ews.helper.wait_for_then_set_text(CopyReprintHelper.max_no_copies, NUMBER_OF_COPIES_SELECTOR_LOCATOR)
        inputElement = ews.helper.wait_for_element_visible((By.ID, 'numberOfCopies'))
        ews.helper.wait_for_then_click('number-plus-button-numberOfCopies')
        current_value = int(inputElement.get_attribute("value"))
        assert  current_value == CopyReprintHelper.max_no_copies, f"Current value: {current_value} not in range min: {CopyReprintHelper.min_no_copies} and max: {CopyReprintHelper.max_no_copies} "

        ews.helper.wait_for_then_set_text(CopyReprintHelper.min_no_copies, NUMBER_OF_COPIES_SELECTOR_LOCATOR)
        ews.helper.wait_for_then_click('number-minus-button-numberOfCopies')
        current_value = int(inputElement.get_attribute("value"))
        assert  current_value == CopyReprintHelper.min_no_copies, f"Current value: {current_value} not in range min: {CopyReprintHelper.min_no_copies} and max: {CopyReprintHelper.max_no_copies} "

        ews.helper.wait_for_then_click('footer-reprint-job-button-cancel')
        queue = job.get_job_queue()
        assert len(queue) == 0
    finally:
        spice.goto_homescreen()
