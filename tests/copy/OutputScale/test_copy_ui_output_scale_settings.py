import logging
import pytest
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting output scale as none
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_output_scale_none
    +test:
        +title: test_copy_ui_adf_landingpage_output_scale_none
        +guid: 309f7135-f3ef-4a84-bd36-f28592a26914
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Print=OutputScale
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_output_scale_none(scan_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'outputScale': 'none'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy settings options for output scale loaded paper
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-118984
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_loaded_paper_scaleToOutput_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_loaded_paper_scaleToOutput_option
        +guid:7ac551d3-858c-464d-a46e-5010a3ab8f9f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & MediaInputInstalled=Main & MediaInputInstalled=MainRoll & MediaInputInstalled=Tray1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ui_loaded_paper_scaleToOutput_option(spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("MDF")
    copy_job_app = spice.copy_ui()

    try:
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.goto_copy_option_output_scale()

        loaded_paper_item = spice.wait_for(CopyAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail)
        loaded_paper_item.mouse_click()
    
        roll_item = spice.query_item(CopyAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_roll+" SpiceText[visible=true]")["text"]
        assert roll_item == "Roll (914 mm)"

        tray_item = spice.query_item(CopyAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_tray+" SpiceText[visible=true]")["text"]
        assert tray_item == "Tray (Letter (8.5x11 in.))"

        select_tray_item = spice.query_item(CopyAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail_tray)
        select_tray_item.mouse_click()
        
        copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
        copy_job_app.back_to_landing_view()
    
    finally:
        spice.goto_homescreen()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy settings output scale Settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141317
    +timeout:270
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_with_output_scale_settings
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_with_output_scale_settings
        +guid:cf269fa5-f29b-4c21-9325-1916e66ef7d7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ADFMediaSize=Letter & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ui_with_output_scale_settings(spice, cdm, udw, net, job, configuration):
    job.bookmark_jobs()

    try:

        copy_job_app = spice.copy_ui()
        options = {
            'outputScale': 'standard_sizes',
            'outputScaleDetailOption': 'a2'
            }
        loadmedia = 'MDF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        
        Copy(cdm, udw).validate_settings_used_in_copy(
        output_scale_standard_size_setting="iso_a2_420x594mm"
        )

        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify string Custom 400% is displayed without any error
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_outputscale_string_verification
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_outputscale_string_verification
        +guid:02b71b97-b66d-4cf0-a6b4-c77402e70005
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FitToPage
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_outputscale_string_verification(setup_teardown_with_copy_job, spice, net):
    copy_job_app = spice.copy_ui()
    logging.info("Go to Copy")
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    logging.info("Go to Options, set Output Scale to Custom 400%")
    copy_job_app.goto_copy_options_list()
    copy_job_app.goto_copy_option_output_scale()
    copy_job_app.goto_copy_output_scale_custom_menu()
    copy_job_app.set_copy_custom_value_option(input_value=400)
    logging.info("Go back Copy Options screen")
    copy_job_app.back_to_copy_options_list_view("Back_to_options_list")

    logging.info("Go back to the previous screen")
    copy_job_app.back_to_landing_view()

    logging.info("Go to Options again, check the value displayed for Output scale option")
    copy_job_app.goto_copy_options_list()
    copy_job_app.verify_copy_settings_selected_option(net, "output_scale", "Custom 400%")
    logging.info("Go back to the previous screen")
    copy_job_app.back_to_landing_view()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify custom option in OutputScale on Click in SpinBoxView 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-202462
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_mdf_outputscale_click_custom_option_in_spinBoxView
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_mdf_outputscale_click_custom_option_in_spinBoxView
        +guid:8f1f103d-5a8d-4680-ad79-a1debb8257e1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & Print=OutputScale
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_mdf_outputscale_click_custom_option_in_spinBoxView(setup_teardown_with_copy_job, spice, net):
    try:
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy")
        copy_job_app.goto_copy_from_copyapp_at_home_screen()
        copy_job_app.goto_copy_options_list()
        copy_job_app.goto_copy_option_output_scale()
        copy_job_app.goto_copy_output_scale_custom_menu(select_option=False)
        custom_option = spice.wait_for(f"{CopyAppWorkflowObjectIds.spinbox_copySettings_outputScale_custom} {CopyAppWorkflowObjectIds.spinBox_numberOfCopies_textArea}")
        custom_option.mouse_click()
        spice.wait_for(CopyAppWorkflowObjectIds.keyboard_view,timeout=20)
        spice.wait_for(CopyAppWorkflowObjectIds.radio_copySettings_outputScale_custom)
        radio_button = spice.wait_for(CopyAppWorkflowObjectIds.radio_copySettings_outputScale_custom)
        radio_button.mouse_click()
        assert(radio_button["checked"] == True)
        copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
        copy_job_app.back_to_landing_view()
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test 2-1 Sided and 2-2 sided is disabled if duplex is not supported in ADF
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-79007
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_duplex_supported_false
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_when_duplex_supported_false
        +guid:7d750ca8-a350-4bdc-b27e-812de0972801
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_when_duplex_supported_false(setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    is_adf_duplex_supported = check_duplex_support(cdm)
    if is_adf_duplex_supported:
        disable_duplex_supported(cdm, udw)
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    spice.goto_homescreen()
    copy_job_app.goto_copy_from_copyapp_at_home_screen()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")

    logging.info("go to sides -> 2 to 1-Sided, and check visibility")
    copy_job_app.check_copy_side_not_visible("2_1_sided") 
    logging.info("go to sides -> 2 to 2-Sided, and check visibility")
    copy_job_app.check_copy_side_not_visible("2_2_sided") 

    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="oneSided",
        orientation="portrait",
        quality="normal",
        content_type="mixed",
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        collate="collated"
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    if is_adf_duplex_supported:
        enable_duplex_supported(cdm, udw)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test constraint message on pages per sheet when output scale is fit to page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-176892
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_adf_pagesPerSheet_constraint_with_outputScale_fitToPage
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_pagesPerSheet_constraint_with_outputScale_fitToPage
        +guid:24a878e8-46b5-4896-ba31-d456775d33d8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & ScannerInput=AutomaticDocumentFeeder & DeviceFunction=Copy & Copy=FitToPage & Copy=2PagesPerSheet & ImagePreview=Refresh

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_adf_pagesPerSheet_constraint_with_outputScale_fitToPage(setup_teardown_with_copy_job,spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app = spice.copy_ui()

    try:
        spice.goto_homescreen()
        copy_job_app.goto_copy_from_copyapp_at_home_screen()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_resize_option("Fit To Page")
        logging.info("Click on pages per sheet option menu and validate the constraint message")
        copy_job_app.validate_pages_persheet_constraint_message(udw, net)
        copy_job_app.back_to_landing_view()

    finally:  
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test 'fit to page' which outputs the original A4 as A3
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-191030
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_adf_outputScale_fitToPage_a4_to_a3
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_outputScale_fitToPage_a4_to_a3
        +guid:eb4a795f-bb1a-4169-b76a-1bbf8e28ded5
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=CopyColor & Copy=FitToPage & MediaSizeSupported=A3   

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_outputScale_fitToPage_a4_to_a3(setup_teardown_with_copy_job, spice, cdm, udw, tray, job):

    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app = spice.copy_ui()

    try:
        if tray.is_size_supported('iso_a3_297x420mm', 'tray-1'):
            tray.configure_tray('tray-1', 'iso_a3_297x420mm', 'stationery')
            tray.load_media('tray-1')
        
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_original_size("A4")
        copy_job_app.select_resize_option("Fit To Page")
        copy_job_app.select_media_size_option("A3 (297x420 mm)")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

        jobHistory = cdm.get(cdm.JOB_HISTORY_ENDPOINT)
        jobId = {key:value for (key,value) in jobHistory["jobList"][-1].items() if key == "jobId"}
        jobId = [jobId["jobId"]][0]

        currentjobStatsEndpoint = cdm.JOB_STAT_ENDPOINT + str(jobId)
        currentjobStats = cdm.get(currentjobStatsEndpoint)

        assert currentjobStats['printInfo']['printSettings']['mediaRequested']['mediaInput']['currentMediaSize'] == "iso_a3_297x420mm", "Job ticket set to A3 should have the output size set to 'iso_a3_297x420mm'"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy settings output scale 'fit to page' Settings 
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-191030
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_adf_outputScale_fitToPage
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_outputScale_fitToPage
        +guid:c63f57e0-c8c5-4080-91b5-05182d88546f
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=CopyColor & Copy=FitToPage

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_outputScale_fitToPage(setup_teardown_with_copy_job,spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app = spice.copy_ui()

    try:
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_original_size("A4")
        copy_job_app.select_resize_option("Fit To Page")
        copy_job_app.select_media_size_option("Letter")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        udwOutput = udw.mainApp.execute("JobTicketResourceManager PUB_getAllJobTicketIDs")
        udwEntries = udwOutput.split("\n")
        assert len(udwEntries) >= 3, "Behavior is undefined for more than 1 job ticket returned from JobTicketResourceManager PUB_getAllJobTicketIDs"

        jobTicketId = udwEntries[-1]

        currentTicketEndpoint = cdm.JOB_TICKET_ENDPOINT + "/" + jobTicketId
        jobTicketOnA4ToLetter = cdm.get(currentTicketEndpoint)

        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["scaleSelection"] == "fitToPage", "Job ticket set to fit To Page should have the scaleSelection set to 'fitToPage'"
        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["fitToPageIncludeMargin"] == "false", "Job ticket set to fit To Page IncludeMargin should have the scaleSelection set to 'fitToPage-IncludeMargin'"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy settings output scale 'fit to page - Include Margin' Settings
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-191030
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_adf_outputScale_fitToPage_includeMargin
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_outputScale_fitToPage_includeMargin
        +guid:5d8bb957-de34-48ac-b68b-8f58c1741ace
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=CopyColor & Copy=FitToPage

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_outputScale_fitToPage_includeMargin(setup_teardown_with_copy_job,spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app = spice.copy_ui()

    try:
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_original_size("A4")
        copy_job_app.select_resize_option("Fit To Page")
        copy_job_app.select_resize_option("Include Margins")
        copy_job_app.select_media_size_option("Letter")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        udwOutput = udw.mainApp.execute("JobTicketResourceManager PUB_getAllJobTicketIDs")
        udwEntries = udwOutput.split("\n")
        assert len(udwEntries) >= 3, "Behavior is undefined for more than 1 job ticket returned from JobTicketResourceManager PUB_getAllJobTicketIDs"

        jobTicketId = udwEntries[-1]

        currentTicketEndpoint = cdm.JOB_TICKET_ENDPOINT + "/" + jobTicketId
        jobTicketOnA4ToLetter = cdm.get(currentTicketEndpoint)

        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["scaleSelection"] == "fitToPage", "Job ticket set to fit To Page should have the scaleSelection set to 'fitToPage'"
        assert jobTicketOnA4ToLetter["pipelineOptions"]["scaling"]["fitToPageIncludeMargin"] == "true", "Job ticket set to fit To Page IncludeMargin should have the scaleSelection set to 'fitToPage-IncludeMargin'"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the combination of 'fit to page' and 'match original'
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-191030
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_adf_outputScale_fitToPage_matchOriginal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_adf_outputScale_fitToPage_matchOriginal
        +guid:bab67ce8-80f8-4092-8fa5-1d170fc4c5e5
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=CopyColor & Copy=FitToPage

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_outputScale_fitToPage_matchOriginal(setup_teardown_with_copy_job,spice, cdm, udw, net, job):
    

    udw.mainApp.ScanMedia.loadMedia("ADF")
    copy_job_app = spice.copy_ui()

    try:
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_original_size("A4")
        copy_job_app.select_resize_option("Fit To Page")
        copy_job_app.select_media_size_option("Match Original Size")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

        jobHistory = cdm.get(cdm.JOB_HISTORY_ENDPOINT)
        jobId = {key:value for (key,value) in jobHistory["jobList"][-1].items() if key == "jobId"}
        jobId = [jobId["jobId"]][0]

        currentjobStatsEndpoint = cdm.JOB_STAT_ENDPOINT + str(jobId)
        currentjobStats = cdm.get(currentjobStatsEndpoint)

        assert currentjobStats['printInfo']['printSettings']['mediaRequested']['mediaInput']['currentMediaSize'] == "iso_a4_210x297mm", "Job ticket set to matchOriginal should have the scaleSelection set to 'matchOriginal'"

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate copy settings options for output scale loaded paper following the display units
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-187107
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_loaded_paper_validate_display_unit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_loaded_paper_validate_display_unit
        +guid:a3d86db3-8d99-4dec-9b9c-95f26a1d50fb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & MediaInputInstalled=ROLL1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
@pytest.mark.disable_autouse
def test_copy_ui_loaded_paper_validate_display_unit(spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("MDF")
    copy_job_app = spice.copy_ui()

    try:
        # setting display unit to imperial
        payload_valid = {
        "version": "1.3.0",
        "countryRegion": "VN",
        "displayUnitOfMeasure":"imperial"
        }
        r = cdm.patch_raw(cdm.SYSTEM_CONFIGURATION_ENDPOINT, payload_valid)
        # Check for a 204 success result
        assert r.status_code == 204
        r = cdm.get_raw(cdm.SYSTEM_CONFIGURATION_ENDPOINT)
        assert r.json()["countryRegion"] == "VN"
        assert r.json()["displayUnitOfMeasure"] == "imperial"

        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.goto_copy_option_output_scale()

        loaded_paper_item = spice.wait_for(CopyAppWorkflowObjectIds.option_output_scale_set_loaded_paper_detail+" #itemContainerTextImage SpiceText[visible=true]")["text"]
        assert loaded_paper_item == "Roll 1 (36.00 in.)"
        
        copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
        copy_job_app.back_to_landing_view()
    
    finally:
        spice.goto_homescreen()
