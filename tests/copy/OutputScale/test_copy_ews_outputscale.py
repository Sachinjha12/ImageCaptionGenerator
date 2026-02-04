import logging
import copy
from tests.copy.copy_ews_combination import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the min and max value for output scale custom
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
    +name:test_copy_ews_outputscale_custom_minimum_value_check
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_outputscale_custom_minimum_value_check
        +guid:1a0a31ce-553d-4e14-b48d-f84044a20876
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Print=OutputScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_outputscale_custom_minimum_value_check(ews):
    #Todo: DUNE-60946:  The error "Check for invalid or missing entries" is displayed instead of "Value too small"
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["scaling"]["xScalePercent"] = 25
        update_expected_settings["pipelineOptions"]["scaling"]["yScalePercent"] = 25
        update_expected_settings["pipelineOptions"]["scaling"]["scaleSelection"] = 'custom'
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set the output scale as 20")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_outputscale_custom_min)
        logging.info("min error message should be shown")
        ews_copy_app.wait_for_min_error_message_displayed()
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("error message should be shown")
        ews_copy_app.wait_for_common_error_message_displayed()
        logging.info("set the output scale as 25")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_outputscale_custom_min_normal)
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("verify the toast info")
        ews_copy_app.applied_success_toast()

        logging.info("check values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the min and max value for output scale custom
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
    +name:test_copy_ews_outputscale_custom_maximum_value_check
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_outputscale_custom_maximum_value_check
        +guid:d074d92c-e720-496d-8198-c26184b0164e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Print=OutputScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_outputscale_custom_maximum_value_check(ews):
    #Todo: DUNE-60946:  The error "Check for invalid or missing entries" is displayed instead of "Maximum value exceeded"
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["scaling"]["xScalePercent"] = 400
        update_expected_settings["pipelineOptions"]["scaling"]["yScalePercent"] = 400
        update_expected_settings["pipelineOptions"]["scaling"]["scaleSelection"] = 'custom'
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set the output scale as 500")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_outputscale_custom_max)
        logging.info("min error message should be shown")
        ews_copy_app.wait_for_max_error_message_displayed()
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("error message should be shown")
        ews_copy_app.wait_for_common_error_message_displayed()
        logging.info("set the output scale as 400")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_outputscale_custom_max_normal)
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("verify the toast info")
        ews_copy_app.applied_success_toast()

        logging.info("check values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
        
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
