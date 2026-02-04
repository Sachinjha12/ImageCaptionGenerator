import logging
from time import sleep
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate Copy Ui Automatic Straighten Setting String
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-153689
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_automatic_straighten_string
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_automatic_straighten_string
        +guid:50f09cbd-3d55-4647-8210-c8855b3a5364
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & CopySettings=AutomaticallyStraighten
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_automatic_straighten_string(setup_teardown_with_copy_job, spice, job, net):
    job.bookmark_jobs()

    try:
        home = spice.main_app.get_home()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        logging.info("go to automatic staighten setting")
        copy_job_app.goto_auto_straighten_settings()
        logging.info("verify the automatic straighten string")
        copy_job_app.workflow_common_operations.verify_string(net, "cAutomaticallyStraighten", CopyAppWorkflowObjectIds.settings_scan_auto_straighten_text, isSpiceText = True)
        copy_job_app.back_to_landing_view()
        
    finally:
        spice.goto_homescreen()
        spice.wait_ready()