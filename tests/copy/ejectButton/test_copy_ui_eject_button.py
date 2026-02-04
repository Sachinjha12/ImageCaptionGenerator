import logging
from time import sleep
from dunetuf.copy.copy import *
from dunetuf.job.job import Job
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy Eject Button Visible for MDF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-157091
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_eject_button
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_eject_button
        +guid:96ce9f95-41cb-4d17-95e7-dede2806b17a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_eject_button(setup_teardown_with_copy_job, spice, job):
    job.bookmark_jobs()

    try:
        home = spice.main_app.get_home()
        spice.main_app.wait_locator_visible(spice.main_app.locators.ui_main_app)
        spice.validate_app(home, False)
        spice.main_app.goto_copy_app()
        
        assert spice.wait_for(CopyAppWorkflowObjectIds.eject_button_detail_panel)

    finally:
        spice.goto_homescreen()
        spice.wait_ready()