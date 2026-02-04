import logging
import copy
import time
from dunetuf.copy.copy import *
from tests.copy.quicksets.copy_combination import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify Copy button Availability is accurate
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-139251
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_copy_widget_availability
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_copy_widget_availability
        +guid:61a6343c-1a66-49de-9fbd-29f4d09fdead
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Widget=Settings & UIComponent=CopyWidget
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_copy_widget_availability(scan_emulation, setup_teardown_with_copy_job, spice, cdm, udw, job):
    #load the ADF
    copy_job_app = spice.copy_ui()
    scan_emulation.media.load_media(media_id='ADF', media_numsheet=10)

    #Start Copy
    logging.info("Set numbers of copies as 2")
    copy_job_app.change_num_copies(num_copies=2)
    logging.info("Click Copy widget start button on Home screen")
    copy_job_app.start_copy_widget()

    job_info_url = job.get_current_job_url("copy")
    current_job_status = job.get_current_job_status(job_info_url)

    #Copy button on homescreen should be unavailable
    prev_copy_button_availability = spice.wait_for(CopyAppWorkflowObjectIds.button_widget_startCopy)["enabled"]
    assert prev_copy_button_availability == False

    #While job is in progress, the copy button should be unavailable
    while current_job_status != "completed":
        copy_button_availability = spice.wait_for(CopyAppWorkflowObjectIds.button_widget_startCopy)["enabled"]
        logging.info("CopyApp Widget start button availability is " + str(copy_button_availability))

        #If the copy button becomes available, it should remain available until the job is completed
        if prev_copy_button_availability == True:
            assert copy_button_availability == True

        time.sleep(1)
        prev_copy_button_availability = copy_button_availability
        current_job_status = job.get_current_job_status(job_info_url)

    logging.info("Change numbers of copies back to 1")
    copy_job_app.change_num_copies(num_copies=1)
    scan_emulation.media.load_media(media_id='ADF', media_numsheet=1)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify value displayed correctly in interactive summary for Copy Quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_quickset_color_interactive_summary
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickset_color_interactive_summary
        +guid:2b884b9a-9714-45a9-bd6e-b9dd3a84fe7d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=2Sided1To2 & Copy=GrayScale

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_quickset_color_interactive_summary(setup_teardown_with_copy_job, ews, spice, net):
    qs = ews.quick_sets_app
    copy_job_app = spice.copy_ui()
    logging.info("Create Copy quickset with Color sets to Grayscale")
    copy_options = copy.deepcopy(copy_option_default)
    copy_options[CopyOptionsKey.color] = CopyOptions.Color.grayscale
    qs.create_copy_quick_sets(
        title=copy_title_name,
        description=copy_description,
        start_option=QuickSetStartOption.start_automatically,
        copy_options=copy_options
    )
    short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
    logging.info("Go to Menu -> Copy")  
    copy_job_app.goto_copy()
    logging.info("Select the created copy quickset")
    copy_job_app.goto_copy_quickset_view()
    copy_job_app.select_copy_quickset("#" + short_cut_id)
    logging.info("Verify the value displayed for Color should be Grayscale")
    copy_job_app.verify_copy_landing_selected_option(net, "color", "grayscale")

    logging.info("Close the current browser")
    ews.close_browser()
    logging.info("Clean up quickset when finish test")
    qs.csc.shortcuts_init(copy_title_name)
