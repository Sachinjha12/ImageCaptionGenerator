from logging import exception
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
import json
import pprint
import logging


def check_duplex_support(cdm):
    response = cdm.get(cdm.SCANNER_STATUS)
    if(response['adf']['duplexSupported'] == 'false'):
        return False
    return True

def enable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(True)
    result = check_duplex_support(cdm)
    assert result == True
    udw.mainApp.ScanMedia.loadMedia("ADF")

def disable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)
    result = check_duplex_support(cdm)
    assert result == False
    udw.mainApp.ScanMedia.loadMedia("ADF")

def check_duplex_support(cdm):
    response = cdm.get(cdm.SCANNER_STATUS)
    if(response['adf']['duplexSupported'] == 'false'):
        return False
    return True

def enable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(True)
    result = check_duplex_support(cdm)
    assert result == True
    udw.mainApp.ScanMedia.loadMedia("ADF")

def disable_duplex_supported(cdm,udw):
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    udw.mainApp.ScanCapabilities.setHasDuplexSupport(False)
    result = check_duplex_support(cdm)
    assert result == False
    udw.mainApp.ScanMedia.loadMedia("ADF")

def verify_copy_default_ticket(cdm):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    # assert 'draft' == ticket_default_body["dest"]["print"]["printQuality"]
    assert 'photo' == ticket_default_body["src"]["scan"]["contentType"]
    assert 'iso_a4_210x297mm' == ticket_default_body["src"]["scan"]["mediaSize"]
    assert 'twoUp' == ticket_default_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
    assert 'grayscale' == ticket_default_body["src"]["scan"]["colorMode"]

def verify_copy_default_ticket_2(cdm):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert 'duplex' == ticket_default_body["src"]["scan"]["plexMode"]
    assert 'tray-2' == ticket_default_body["dest"]["print"]["mediaSource"]
    #assert 'na_legal_8.5x14in' == ticket_default_body["dest"]["print"]["mediaSize"]
    assert 'stationery' == ticket_default_body["dest"]["print"]["mediaType"]
    assert 8 == ticket_default_body["pipelineOptions"]["imageModifications"]["exposure"]
    assert 'uncollated' == ticket_default_body["dest"]["print"]["collate"]
    assert 'true' == ticket_default_body["src"]["scan"]["pagesFlipUpEnabled"]


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test Color copy with Content type sets to Text
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_using_content_type_and_color
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_using_content_type_and_color
        +guid:cb7d0252-6bb9-457c-8fce-7a29a8e28401
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale & ScanContentType=Text
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_job_using_content_type_and_color(setup_teardown_with_copy_job, scan_emulation, job, spice, net, cdm, udw, configuration):
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    else:
        scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    if configuration.productname in ["jupiter", "beam/beamsfp_power", "beam/beammfp_power"]:
        contentOption = "Lines"
    else:
        contentOption = "Text"
    logging.info("go to content type screen and check the strings")
    copy_job_app.goto_copy_option_content_type_screen()
    copy_job_app.check_spec_on_copy_options_content_type(net, configuration) 
    logging.info("set the content type to " + contentOption)
    copy_job_app.select_content_type(contentOption)
    if cdm.device_feature_cdm.is_color_supported():
        logging.info("go to color screen and check the strings")
        copy_job_app.goto_copy_option_color_screen()
        copy_job_app.check_spec_on_copy_options_color(net)
        logging.info("set the color to grayscale")
        copy_job_app.select_color_mode("Grayscale")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy()
    if job.job_concurrency_supported == "false":
        copy_job_app.wait_for_release_page_prompt_and_click_relasePage()

    if configuration.productname in ["jupiter", "beam/beamsfp_power", "beam/beammfp_power"]:
        Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        color_mode="grayscale",
        content_type="lineDrawing",
        tray_setting="auto",
        quality="normal",
        sides="oneSided",
        orientation="portrait",
        two_side_page_flip_up="false", 
        pages_per_sheet="oneUp"
        )
    else:
        Copy(cdm, udw).validate_settings_used_in_copy(
            number_of_copies=1,
            color_mode="grayscale",
            content_type="text",
            tray_setting="auto",
            quality="normal",
            sides="oneSided",
            orientation="portrait",
            two_side_page_flip_up="false", 
            pages_per_sheet="oneUp",
            collate="collated"
        )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    #spice.go_to_homescreen()
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with combined settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:700
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_miscellaneous_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_miscellaneous_values
        +guid:1c22e590-0460-41d2-888a-eb46a69691c7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation & Copy=2Sided2To2 
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_job_with_miscellaneous_values(ews,setup_teardown_with_copy_job, scan_emulation, spice, net, job, cdm, udw, configuration):
    scan_emulation.media.load_media(media_id='ADF')
    is_adf_duplex_supported = spice.copy_ui().check_duplex_support(cdm)
    if is_adf_duplex_supported == False:
        spice.copy_ui().enable_duplex_supported(cdm, udw)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("set the number as 5")
    copy_job_app.ui_copy_set_no_of_pages(value=5)
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    copy_job_app.select_copy_side("2_2_sided")
    logging.info("set the content type to Photograph")
    copy_job_app.select_content_type("Photograph")
    logging.info("set flip up as ON")
    copy_job_app.set_copy_2sided_flip_up_options(two_sided_options="on")
    copy_job_app.select_original_size("Letter")
    if color_supported is True:
        logging.info("set color mode to Color")
        copy_job_app.select_color_mode("Color")
    
    # For Mono model, there is no Color mode option.
    # Even in the case of color models, if remove the color permission from the Printer Feature of EWS, 
    # this behavior is removed because Grayscale is selected by default in the UI.
    # else:
    #     logging.info("set color mode to Grayscale")
    #     copy_job_app.select_color_mode("Grayscale")

    logging.info("set the lighter and darker value is 9")
    copy_job_app.select_scan_settings_lighter_darker(lighter_darker=9, dial_value=180)
    logging.info("go to output scale option")
    copy_job_app.goto_copy_option_output_scale()
    logging.info("go to custom screen")
    copy_job_app.goto_copy_output_scale_custom_menu()
    logging.info("set the value of custom")
    copy_job_app.set_copy_custom_value_option(input_value=400)
    logging.info("Back to the options screen")
    copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
    # logging.info("Set Quality mode to Best")
    # copy_job_app.select_quality_option("Best")
    time.sleep(6)
    logging.info("Verify that page per sheet option is constrained")
    copy_job_app.verify_copy_pages_per_sheet_constrained(udw, net)
    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    time.sleep(6)
    logging.info("Start to copy")
    copy_job_app.start_copy()

    scaleToFitEnabled = 'false'
    if configuration.familyname == 'enterprise':
        scaleToFitEnabled = 'true'

    #time.sleep(5)
    if color_supported is True:
        Copy(cdm, udw).validate_settings_used_in_copy(
            number_of_copies=5,
            color_mode="color",
            original_size="na_letter_8.5x11in",
            tray_setting="auto",
            sides="twoSidedShortEdge",
            orientation="portrait",
            # quality="best",
            content_type="photo",
            pages_per_sheet="oneUp",
            collate="collated",
            lighter_darker=9,
            output_scale_setting = {'scaleToFitEnabled': scaleToFitEnabled, 'xScalePercent': 400, 'yScalePercent': 400, 'scaleSelection': 'custom'}
        )
    else:
        Copy(cdm, udw).validate_settings_used_in_copy(
            number_of_copies=5,
            color_mode="grayscale",
            original_size="na_letter_8.5x11in",
            tray_setting="auto",
            sides="twoSidedShortEdge",
            orientation="portrait",
            # quality="best",
            content_type="photo",
            pages_per_sheet="oneUp",
            collate="collated",
            lighter_darker=9,
            output_scale_setting = {'scaleToFitEnabled': scaleToFitEnabled, 'xScalePercent': 400, 'yScalePercent': 400, 'scaleSelection': 'custom'}
        )
    
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Complete', timeout=90)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    if is_adf_duplex_supported == False:
        spice.copy_ui().disable_duplex_supported(cdm, udw)
    scan_emulation.media.unload_media('ADF')

    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy options ContentType, Original Size, ColorMode, PagesPerSheet
    +test_tier:1
    +is_manual:False
    +reqid:DUNE
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option
        +guid:53bdb944-1d64-4a84-b126-0bf8c0fb389c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option(job, net, udw, spice, cdm):

    # check jobId
    udw.mainApp.ScanMedia.loadMedia("ADF")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy2", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_options_list()

        # set copy options
        spice.copy_ui().select_content_type("Photograph")
        spice.copy_ui().select_color_mode("Grayscale")
        spice.copy_ui().select_original_size("A4")
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        # spice.copy_ui().select_quality_option("Draft")

        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()
        time.sleep(5)

        #verify default ticket value
        ticket_default_body = Copy.get_copy_default_ticket(cdm)
        # assert 'draft' == ticket_default_body["dest"]["print"]["printQuality"]
        assert 'photo' == ticket_default_body["src"]["scan"]["contentType"]
        assert 'iso_a4_210x297mm' == ticket_default_body["src"]["scan"]["mediaSize"]
        assert 'twoUp' == ticket_default_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
        assert 'grayscale' == ticket_default_body["src"]["scan"]["colorMode"]

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        if spice.universal_sign_in_app.is_signed_in():
            spice.universal_sign_in_app.sign_out()
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for ADF simple Job cancel
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-156734
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_ADF_simple_Job_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_ADF_simple_Job_cancel
        +guid:9a44de47-66dc-4702-9707-9bff47d9c2c4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_ADF_simple_Job_cancel(setup_teardown_with_copy_job, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")

    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    
    logging.info("Start a copy job")
    copy_job_app.start_copy()

    logging.info("Click Cancel button")
    current_option = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_button)
    current_option.mouse_click()  

    time.sleep(5)

    logging.info("Check the copy job cancelled successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration, message='Cancel')
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
    spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify copy jobdetails from ui
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_copy_jobdetails_from_ui
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:JobDetails
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_copy_jobdetails_from_ui
        +guid:8b0316b9-d63f-447f-acfc-9d74f134057c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_copy_jobdetails_from_ui(cdm, job, spice, udw, scan_emulation):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    scan_emulation.media.load_media(media_id='ADF') 
    # udw.mainApp.ScanMedia.loadMedia("ADF")

    try:
        # Go to copy app and start copy job
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()

        # Wait for the job to complete and get the job id.
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)

        # Go to Homescreen and Job Queue App screen
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()

        # Check that the job is in "History" section
        spice.job_ui.goto_job(job_id_cdm)
        assert spice.job_ui.recover_job_status() == "Completed"

        # Check by CDM that the job has passed to history
        job_cdm = job.get_job_from_history_by_id(job_id_cdm)
        assert job_cdm["jobId"] == job_id_cdm
        time.sleep(3)
        #Validate job details from UI side
        assert spice.job_ui.recover_job_total_pages() , "Total Pages not found"
        assert spice.job_ui.recover_job_copies() , "copies not found"
        assert spice.job_ui.recover_job_start_time()[0:-4] , "Started time not found"
        assert spice.job_ui.recover_job_completion_time()[0:-4] , "Completed time not found"
        assert spice.job_ui.recover_job_user_name() , "username not found"
        assert spice.job_ui.recover_job_type() , "job type not found"
        assert spice.job_ui.recover_job_media_source(), "source not found"
        assert spice.job_ui.recover_job_media_tpye(), "media type not found"
        assert spice.job_ui.recover_job_output_size(), "output size not found"
        assert spice.job_ui.recover_job_color_mode() , "color mode not found"
        assert spice.job_ui.recover_job_quality() , "quality not found"
        assert spice.job_ui.recover_job_original_size() , "original size not found"
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify the copy job with adf with settings paper size letter and paper type glossy.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_adf_verify_paper_size_letter_paper_type_glossy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_verify_paper_size_letter_paper_type_glossy
        +guid:599d4687-be3e-4233-8c21-0b121cf937af
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=PaperType & MediaType=HPBrochureGlossy150g & ADFMediaSize=Letter
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_verify_paper_size_letter_paper_type_glossy(job, spice, cdm, udw, net):
    job.bookmark_jobs()
    job.clear_joblog()
    try:
        spice.goto_homescreen()
        copy_job_app = spice.copy_ui()
        options = {
            'paper_selection': {
                'paper_size': 'Letter',
                'paper_type': 'HP Glossy (150g)'
            }
        }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        response = cdm.get_raw(cdm.JOB_STAT_ENDPOINT + job_id)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        #paper size and paper type validation
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaSizeId'] == 'na_letter_8.5x11in', "Paper size mismatch"
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['mediaTypeId'] == 'com.hp.glossy-160gsm', "Paper type mismatch"
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify whether the background cleanup slider value is consistent or not if we set more than 9
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-231411
    +timeout: 360
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test_classification: System
    +name: test_copy_ui_background_cleanup_value_is_consistent_or_not_if_we_set_more_than_9
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_background_cleanup_value_is_consistent_or_not_if_we_set_more_than_9
        +guid: 97663405-a238-4d23-ab63-7927a05a3151
        +dut:
            +type: Simulator
            +configuration: DeviceFunction=Copy & ScanSettings=BackgroundCleanup
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_background_cleanup_value_is_consistent_or_not_if_we_set_more_than_9(setup_teardown_with_copy_job, spice, job, udw, net):
    try:
        job.bookmark_jobs()
        copy_job_app = spice.copy_ui()
        spice.goto_homescreen()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        # Set the background cleanup value to 9 and verify value is 9 or not once we go back to copy landingview and go back to options page
        copy_job_app.set_background_cleanup_setting_value('9')
        copy_job_app.verify_background_cleanup_setting_value('9')
        copy_job_app.back_to_landing_view()
        copy_job_app.goto_copy_options_list()
        copy_job_app.verify_background_cleanup_setting_value('9')
        copy_job_app.back_to_landing_view()
    finally:
        spice.goto_homescreen()

