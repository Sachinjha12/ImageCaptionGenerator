import logging
from tests.copy.ews.copy_default_settings.copy_ews_combination import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test color mode selection settings Automatic in copy settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_colorMode_automatic
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_colorMode_automatic
        +guid:6c7f277e-92b1-472a-b42f-b6390d934b01
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & DeviceFunction=CopyColor

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_colorMode_automatic(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["colorMode"] = "autoDetect"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set color mode values as automatic")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_colorMode_automatic)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test color mode selection settings Color in copy settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_colorMode_color
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_colorMode_color
        +guid:f2c11656-a40e-4a71-a104-63d75adbbd40
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & DeviceFunction=CopyColor

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_colorMode_color(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["colorMode"] = "color"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set color mode values as automatic")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_colorMode_color)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test color mode selection settings Grayscale in copy settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_colorMode_grayscale
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_colorMode_grayscale
        +guid:9c187536-cbf7-4bbf-95b0-e932c661d32b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & DeviceFunction=CopyColor

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_colorMode_grayscale(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["colorMode"] = "grayscale"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set color mode values as automatic")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_colorMode_grayscale)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
