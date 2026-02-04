import logging
from dunetuf.copy.copy import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test id card copy job with grayscale and best
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-120486
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_job_with_grayscale_best
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard_job_with_grayscale_best
        +guid:179446c3-95f5-45fe-afd2-84e492ab6b70
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale & Copy=Quality & Copy=IDCopy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard_job_with_grayscale_best(setup_teardown_with_id_copy_job, job, spice, net, cdm, udw):
    job.bookmark_jobs()
    logging.info("Go to id copy screen")
    idcopy_job_app = spice.idcard_copy_app
    idcopy_job_app.goto_idcopy()
    logging.info("Go to ID Card Copy -> Options screen")
    idcopy_job_app.goto_copy_options_list()
    logging.info("Go to ID Card Copy -> Options -> Color screen")
    idcopy_job_app.goto_idcopy_option_color_screen()
    logging.info("Set Color mode to Color")
    idcopy_job_app.set_idcopy_color_options(net, "Grayscale")
    logging.info("Go to ID Card Copy -> Options -> Quality screen")
    idcopy_job_app.goto_quality_option(dial_value=0)
    logging.info("Set Quality to Best")
    idcopy_job_app.set_idcopy_quality_options(net, idcopy_quality_options="Best")
    logging.info("Go back ID Copy Landing screen from Options screen")
    idcopy_job_app.back_to_landing_view()
    logging.info("Start ID Card copy")
    idcopy_job_app.start_id_copy(dial_value=0)
    logging.info("Select continue button")
    idcopy_job_app.select_idcopy_first_continue_button()
    logging.info("Select second continue button")
    idcopy_job_app.select_idcopy_second_continue_button()
    logging.info("verify the value used for job using cdm")
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        quality="best"
    )
    logging.info("wait for the id card copy job complete")
    idcopy_job_app.wait_for_idcopy_complete(net)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}])


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test id card copy job with some settings
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_job_with_miscellaneous_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard_job_with_miscellaneous_values
        +guid:007f091b-321b-43fd-8d41-1f00d2c48c94
        +dut:
            +type:Engine
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=Tray2 & Copy=IDCopy & Copy=Quality


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard_job_with_miscellaneous_values(setup_teardown_with_id_copy_job, job, spice, net, cdm, udw):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    copy_job_app = spice.copy_ui()
    options = {
            'colorMode': 'Color',
            'tray': 'Tray 2',
            'lighter_darker': '9',
            'quality': 'Best'
        }
    loadmedia='Flatbed'
    copy_path = 'IDCardLandingPage'
    copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)

    logging.info("verify the value used for job using cdm")
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="tray-2",
        lighter_darker=9,
        quality="best"
    )
    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copies and printed pages in idcopy job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_verify_copies_printed_pages_in_idcopy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_copies_printed_pages_in_idcopy_job
        +guid:29052706-7475-46aa-80d7-16f6a3dfb042
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_copies_printed_pages_in_idcopy_job(spice, cdm, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    #Load one page on Flatbed for IDCard Job
    scan_emulation.media.load_media('Flatbed', 1)
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'copies':'1'
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        ENDPOINT = cdm.JOB_STAT_ENDPOINT + job_id
        response = cdm.get_raw(ENDPOINT)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['printInfo']['copiesCount'] == 1 , "Number of copies count mismatch"
        assert cdm_response['printInfo']['printedSheetInfo']['sheetSet'][0]['count'] == 1 , "Incorrect printedSheetInfo count"
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Set copies, quality and color in document copy and Verify copies, quality and color in idcopy job.
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_set_2copies_quality_best_color_grayscale_verify_in_idcopy_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_set_2copies_quality_best_color_grayscale_verify_in_idcopy_job
        +guid:2b4dea04-bc82-4a17-a06c-1943f3e2322d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=IDCopy & Copy=GrayScale & Copy=Quality & CopyColorMode=Grayscale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_set_2copies_quality_best_color_grayscale_verify_in_idcopy_job(setup_teardown_with_id_copy_job, spice, cdm, job, udw, net):
    job.bookmark_jobs()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)
    try:
        logging.info("Go to copy screen")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.ui_copy_set_no_of_pages(2)
        copy_job_app.select_color_mode("Grayscale")
        logging.info("Set Copy Quality to Best")
        copy_job_app.select_quality_option("Best")
        logging.info("Back to copy screen")
        copy_job_app.back_to_landing_view()
        copy_job_app.save_as_default_copy_ticket()
        spice.goto_homescreen()
        job.clear_joblog()
        logging.info("Go to idcopy")
        spice.idcard_copy_app.goto_idcopy()
        spice.idcard_copy_app.start_copy()
        logging.info("wait for the id card copy job complete")
        spice.idcard_copy_app.wait_for_idcopy_complete(net)
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm() 
        logging.info('job_id,', job_id)
        #Read Data from stats Job 
        ENDPOINT = cdm.JOB_STAT_ENDPOINT + job_id
        response = cdm.get_raw(ENDPOINT)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        #verify job name and above settings
        assert cdm_response['jobInfo']['jobName'] == 'IDCardCopy' , "job name is mismatch"
        assert cdm_response['printInfo']['copiesCount'] == 2 , "number for copies mismatch"
        assert cdm_response['printInfo']['printSettings']['colorMode'] == 'grayscale' , 'Color is mismatch'
        assert cdm_response['printInfo']['printSettings']['printQuality'] == 'best' , 'print quality mismatch'
        
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)

    