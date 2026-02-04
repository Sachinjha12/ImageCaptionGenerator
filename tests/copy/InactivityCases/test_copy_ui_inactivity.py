import logging
import uuid
import pytest
from dunetuf.ssh import SSH
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from tests.ui.lib.actions.commonsActions import *
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate that the number of copies user-set reset to default values
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-145486
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_widget_change_num_copies_and_verify_num_copies_on_inactivity_timeout
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_widget_change_num_copies_and_verify_num_copies_on_inactivity_timeout
        +guid:06ad0a84-a37d-47f0-9cc0-4d3a6342befb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & InactivityTimeout=5Minutes  & UIComponent=CopyWidget         
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_num_copies_and_verify_num_copies_on_inactivity_timeout(spice, cdm, udw, tcl, job, copy,setup_teardown_print_device):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    expected_number_of_default_copies = 1

    udw.mainUiApp.ApplicationEngine.setInactivityTimerinSeconds(30)

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Change number of copies
    # increase to 2 and verify whether the widget is updated to 2 or not
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == 2

    # increase to 3 and verify whether the widget is updated to 3 or not
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == 3

    # increase to 4 and verify whether the widget is updated to 4 or not
    spice.copy_ui().increase_widget_num_copies(SINGLE_COPY_COUNT_INCREMENT)
    assert spice.copy_ui().get_number_of_widget_copies() == 4

    # validate incremented counts
    sleep(50)
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Check the copy Count in the widget. Should match what we set it to!:
    assert spice.copy_ui().get_number_of_widget_copies() == expected_number_of_default_copies
