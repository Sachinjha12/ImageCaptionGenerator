import logging
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with Fit to Page setting
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_using_output_scale_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_using_output_scale_option
        +guid:9b311d1a-0ad6-49db-8b1f-396b2525c866
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FitToPage & Copy=ImagePreview
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_job_using_output_scale_option(setup_teardown_with_copy_job, scan_emulation, job, spice, net, cdm, udw, configuration):
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("go to output scale and check the strings")
    copy_job_app.goto_copy_option_output_scale()
    copy_job_app.check_spec_copy_options_output_scale(net)
    logging.info("set the fit to page to output scale")
    copy_job_app.select_resize_option("Fit To Page")
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    logging.info("Back to copy screen")
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
        collate="collated",
        output_scale_setting = {'scaleToFitEnabled': 'true', 'xScalePercent': 100, 'yScalePercent': 100, 'scaleSelection': 'fitToPage'})
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    '''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with Custom 200% after checking value range
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_with_output_scale_custom_value
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_with_output_scale_custom_value
        +guid:9124e9a3-af07-4ad4-a511-046c9755ce57
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FitToPage
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_with_output_scale_custom_value(scan_emulation, setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration): 
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    if "mdf" in udw.mainApp.ScanMedia.listInputDevices().lower():
        udw.mainApp.ScanMedia.loadMedia("MDF")
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("go to output scale option")
    copy_job_app.goto_copy_option_output_scale()

    logging.info("go to custom screen")
    copy_job_app.goto_copy_output_scale_custom_menu()
    logging.info("set the value of custom to 20")
    copy_job_app.set_copy_custom_value_option(input_value=20)

    #logging.info("go to custom screen")
    #copy_job_app.goto_copy_output_scale_custom_menu()
    logging.info("set the value of custom to 500")
    copy_job_app.set_copy_custom_value_option(input_value=500)

    #logging.info("go to custom screen")
    #copy_job_app.goto_copy_output_scale_custom_menu()
    logging.info("set the value of custom to 200")
    copy_job_app.set_copy_custom_value_option(input_value=200)

    logging.info("Back to the options screen")
    copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
    logging.info("Back to the copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    if job.job_concurrency_supported == "false":
        copy_job_app.wait_for_release_page_prompt_and_click_relasePage()
    
    scaleToFitEnabled = 'false'
    if configuration.familyname == 'enterprise':
        scaleToFitEnabled = 'true'

    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="oneSided",
        orientation="portrait",
        quality="normal",
        content_type="mixed", 
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        output_scale_setting = {'scaleToFitEnabled': scaleToFitEnabled, 'xScalePercent': 200, 'yScalePercent': 200, 'scaleSelection': 'custom'}
    )
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy settings for output scale standard sizes
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:300
    +asset:LFP
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_with_output_scale_standardsizes_values
    +test:
        +title:test_copy_ui_with_output_scale_standardsizes_values
        +guid:1adf710b-98be-4bc9-a6d8-7e01d54ba2dd
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ui_with_output_scale_standardsizes_values(setup_teardown_with_copy_job,spice, cdm, udw, net, job):
    udw.mainApp.ScanMedia.loadMedia("MDF")
    copy_job_app = spice.copy_ui()

    try:
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        copy_job_app.goto_copy_option_output_scale()
        copy_job_app.set_output_scale_options(net, output_scale_options="standard_sizes", detail_option="letter")
        logging.info("Back to the options screen")
        copy_job_app.back_to_copy_options_list_view("Back_to_options_list")
        copy_job_app.back_to_landing_view()
        copy_job_app.goto_copy_options_list()
        copy_job_app.homemenu.menu_navigation(spice,CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_outputScale,select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        logging.info("go to copy settings and check the strings selected against output_scale")
        copy_job_app.check_spec_on_usb_print_options_output_scale(net, output_scale="Standard Sizes")
        copy_job_app.back_to_landing_view()
    
    finally:
        spice.goto_homescreen()
