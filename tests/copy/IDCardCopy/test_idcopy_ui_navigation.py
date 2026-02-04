import logging
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
import time
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test id card copy simple job
    +test_tier:1
    +is_manual:False
    +reqid:DUNE
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_id_card
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_id_card
        +guid:6761ddb9-0576-42a7-be13-8ec138eeb57a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & Copy=IDCopy
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_copy_ui_id_card(job, udw, spice):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        spice.idcard_copy_app.goto_idcopy()
        spice.idcard_copy_app.start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test id card copy options ContentOrientation, Tray, ColorMode, Lighter/Darker, Quality
    +test_tier:1
    +is_manual:False
    +reqid:DUNE
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui__id_card_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui__id_card_option
        +guid:8c78bb6d-5d77-4e1d-b749-0acb8d438110
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & Copy=IDCopy & Copy=PaperTray
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui__id_card_option(job, udw, spice, cdm):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        spice.idcard_copy_app.goto_idcopy()
        spice.idcard_copy_app.set_copy_settings(cdm)
        spice.idcard_copy_app.back_to_landing_view()
        spice.idcard_copy_app.start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test id card copy with default values
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard__happy_path_default_values
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard__happy_path_default_values
        +guid:b645e69b-3711-41de-9c2e-352bf7d7000e
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy & MediaInputInstalled=Automatic


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard__happy_path_default_values(setup_teardown_with_id_copy_job, job, spice, net, cdm, udw):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to id copy screen")
    idcopy_job_app = spice.idcard_copy_app
    idcopy_job_app.goto_idcopy()
    logging.info("start to id card copy")
    time.sleep(3)
    idcopy_job_app.start_id_copy()
    logging.info("check the first screen message and select continue")
    idcopy_job_app.check_spec_on_idcopy_first_screen(net)
    idcopy_job_app.select_idcopy_first_continue_button()

    logging.info("check the second screen message and select second continue")
    idcopy_job_app.check_spec_on_idcopy_second_screen(net)
    idcopy_job_app.select_idcopy_second_continue_button()

    logging.info("verify the value used for job using cdm")
    Copy(cdm, udw).validate_settings_used_in_copy(number_of_copies=1, tray_setting="auto", orientation="portrait")
    logging.info("wait for the id card copy job complete")
    idcopy_job_app.wait_for_idcopy_complete(net)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}])

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the return from menu_idCardCopy
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcard_navigation_from_home_idcardcopy
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcard_navigation_from_home_idcardcopy
        +guid:1e687ee2-4cd9-4985-a048-2237d9facdde
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''


def test_copy_ui_idcard_navigation_from_home_idcardcopy(setup_teardown_with_id_copy_job, job, spice, net):
    logging.info("Go to id copy screen")
    idcopy_job_app = spice.idcard_copy_app
    idcopy_job_app.goto_idcopy()
    logging.info("back to the home screen")
    idcopy_job_app.back_to_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test id card copy simple job from home screen
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-118509
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_idcardhomescreen
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_idcardhomescreen
        +guid:7ef54b7d-336c-4678-976a-fa0ef1d7578e
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_idcardhomescreen(job,udw,net, spice):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()

    try:
        spice.idcard_copy_app.goto_idcopy_fromhomescreen()
        idcopy_job_app = spice.idcard_copy_app
        idcopy_job_app.ui_idcopy_set_no_of_pages(5)
        idcopy_job_app.goto_copy_options_list()
        idcopy_job_app.goto_idcopy_option_color_screen()
        idcopy_job_app.set_idcopy_color_options(net, idcopy_color_options="Grayscale")
        idcopy_job_app.back_to_landing_view()
        spice.idcard_copy_app.start_copy()
        copy_job_id = job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Job Modal Status Header in ID Card Copy Job
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-120453
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_idcopy_ui_job_modal_status_header
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_job_modal_status_header
        +guid: 554661c3-5eab-465b-88cd-bf262ebebb2a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=IDCopy & ScannerInput=Flatbed & ImagePreview=Refresh & JobType=NonConcurrent
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_job_modal_status_header(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        active_job_modal_header = copy_job_app.workflow_common_operations.get_expected_translation_str_by_str_id(net, 'cIDCardCopyApp')
        header_modal_status = spice.query_item(CopyAppWorkflowObjectIds.copy_active_job_modal_header_text_locator)["text"]
        assert active_job_modal_header == header_modal_status
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
