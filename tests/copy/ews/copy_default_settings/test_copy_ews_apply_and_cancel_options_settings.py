import logging
import time
from tests.copy.ews.copy_default_settings.copy_ews_combination import *


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:veify the toast info after click apply button
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_apply_button
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_apply_button
        +guid:ae58a049-d37c-43e2-814a-265e3b0f622c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_apply_button(ews):
    try:
        ews_copy_app = ews.copy_ews_app
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("verify the toast info")
        ews_copy_app.applied_success_toast()
    finally:
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the values after click cancel button
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_cancel_button
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_cancel_button
        +guid:7b78a6dc-2131-4cd3-aa2b-c5ef7c232fe5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & JobSettings=EWSJobQueue

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_cancel_button(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("get the values for element")
        element_value = ews_copy_app.get_current_values_of_options_from_page()
        logging.info("set the options for copy")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_random)
        ews_copy_app.click_ews_copy_page_cancel_button()
        time.sleep(10)
        logging.info("check values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
        logging.info("get the values for element again")
        update_element_value = ews_copy_app.get_current_values_of_options_from_page()
        logging.info("compare the data before and after")
        assert element_value == update_element_value, "options values are different"
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
