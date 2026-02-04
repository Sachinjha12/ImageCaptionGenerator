import logging
import copy
from dunetuf.copy.copy import *
from tests.copy.ews.copy_default_settings.copy_ews_combination import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original SEF size and verify values by cdm and UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_default_setting_originalsize_SEF_A4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_ui_default_setting_originalsize_SEF_A4
        +guid:6d4d1365-db1f-436e-80aa-9f06e8227fa0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & Copy=OriginalSize & Copy=IDCopy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ews_ui_default_setting_originalsize_SEF_A4(ews, spice, net):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF A4(210x297mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_SEF_A4)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

        logging.info("Go to Menu -> Copy -> Copy option list")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for Original Size or Paper Size")
        copy_job_app.verify_copy_mediasize_selected_option(net, "original", "A4_SEF")



    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
        copy_job_app.back_to_landing_view()
        spice.goto_homescreen()
        spice.wait_ready()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper SEF size and verify values by cdm and UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_default_setting_papersize_SEF_A4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_ui_default_setting_papersize_SEF_A4
        +guid:2eb3f538-a96b-4a7d-9bd3-cfdce8c32ec1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ews_ui_default_setting_papersize_SEF_A4(ews, spice, net):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set paper size values as SEF A4(210x297mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_SEF_A4)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

        logging.info("Go to Menu -> Copy -> Copy option list")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for paper Size or Paper Size")
        copy_job_app.verify_copy_mediasize_selected_option(net, "paper", "A4_SEF")



    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
        copy_job_app.back_to_landing_view()
        spice.goto_homescreen()
        spice.wait_ready()
        
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Set the default value of Auto tone to 5 in EWS and verify this with UI and CDM.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-191053
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_default_setting_auto_tone
    +test:
        +title:test_copy_ews_ui_default_setting_auto_tone
        +guid:79433f91-edcc-4d2a-8fe1-b2c25e581829
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutomaticTone
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ews_ui_default_setting_auto_tone(ews, spice):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["autoTone"] = "true"
        update_expected_settings["pipelineOptions"]["imageModifications"]["autoToneLevel"] = 5
        
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        
        logging.info("set auto tone values to 5")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_auto_tone_level_5)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

        logging.info("Go to Menu -> Copy -> Copy option list")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for Auto Tone or Auto paper color removal")
        copy_job_app.verify_copy_auto_tone_paper_color_option(auto_tone_checkbox_val=True, auto_tone_slider_val=5)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
        copy_job_app.back_to_landing_view()
        spice.goto_homescreen()
        spice.wait_ready()
        
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Set the default value of Auto Paper Color Removal to 5 in EWS and verify this with UI and CDM.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-191053
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_default_setting_auto_paper_color_removal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_ui_default_setting_auto_paper_color_removal
        +guid:f44c05f5-07b1-4717-ba68-a1b4ead30a39
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutoPaperColorRemoval
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ews_ui_default_setting_auto_paper_color_removal(ews, spice):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["autoPaperColorRemoval"] = "true"
        update_expected_settings["pipelineOptions"]["imageModifications"]["autoPaperColorRemovalLevel"] = 5
        
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        
        logging.info("set auto paper color removal values to 5")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_auto_paper_color_level_5)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

        logging.info("Go to Menu -> Copy -> Copy option list")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for Auto Tone or Auto paper color removal")
        copy_job_app.verify_copy_auto_tone_paper_color_option(auto_paper_color_checkbox_val=True, auto_paper_color_slider_val=5)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
        copy_job_app.back_to_landing_view()
        spice.goto_homescreen()
        spice.wait_ready()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size(letter) and paper type(palin) from ews copy settings, verify copy job and validate paper size(letter) and paper type(plain). 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_verify_copy_job_with_settings_paper_size_letter_paper_type_plain
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_ui_verify_copy_job_with_settings_paper_size_letter_paper_type_plain
        +guid:1124a28e-3216-4801-b184-ea97cb3699f3
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=PaperSize & ADFMediaSize=Letter & JobSettings=EWSJobQueue & Copy=PaperType & MediaType=Plain

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_ui_verify_copy_job_with_settings_paper_size_letter_paper_type_plain(ews, spice, cdm, job):
    job.bookmark_jobs()
    job.clear_joblog()
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_diffrent_combination_papersize_papertype_combi_one)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("Go to Menu -> Copy -> Copy Landing view")
        copy_job_app.goto_copy()
        logging.info("Start a copy job")
        copy_job_app.start_copy()
        logging.info("Click Cancel button")
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT  + job_id)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        #paper size and paper type validation
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaSizeId'] == 'na_letter_8.5x11in', "Paper size mismatched"
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaTypeId'] == 'stationery', "Paper type mismatched"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        ews.close_browser()
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size(legal) and paper type(palin) from ews copy settings, verify copy job and validate paper size(legal) and paper type(plain). 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_ui_verify_copy_job_with_settings_paper_size_legal_paper_type_plain
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_ui_verify_copy_job_with_settings_paper_size_legal_paper_type_plain
        +guid:8ea3da34-917b-4142-9090-477e2a4df4a9
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & JobSettings=EWSJobQueue & Copy=PaperSize & ADFMediaSize=Legal & ScannerInput=AutomaticDocumentFeeder & Copy=PaperType & MediaType=Plain
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_ui_verify_copy_job_with_settings_paper_size_legal_paper_type_plain(ews, spice, cdm, job, udw):
    job.bookmark_jobs()
    job.clear_joblog()
    udw.mainApp.ScanMedia.loadMedia("ADF")
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    copy_job_app = spice.copy_ui()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_diffrent_combination_papersize_papertype_combi_two)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("Go to Menu -> Copy -> Copy option list")
        copy_job_app.goto_copy()
        logging.info("Start a copy job")
        copy_job_app.start_copy()
        logging.info("Click Cancel button")
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT  + job_id)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        #paper size and paper type validation
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaSizeId'] == 'na_legal_8.5x14in', "Paper size mismatched"
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaTypeId'] == 'stationery', "Paper type mismatched"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        ews.close_browser()
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
