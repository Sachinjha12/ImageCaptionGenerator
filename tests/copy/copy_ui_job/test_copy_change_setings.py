import logging
import pytest
from time import sleep
from typing import ClassVar

from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test paper selection values in copy settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-140846
    +timeout:220
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_check_paper_selection_value
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_check_paper_selection_value
        +guid:0e55fa77-9d08-4ff1-a2da-5b020721ca85
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_check_paper_selection_value(setup_teardown_with_copy_job,spice):

    try:   
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.homemenu.menu_navigation(spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_paperSelection, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        get_paper_selection_string = spice.wait_for(CopyAppWorkflowObjectIds.view_paperSetting + " SpiceText[visible=true]")["text"]
        copy_job_app.go_to_paper_selection()
        paper_size = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSize + " SpiceText[visible=true]")["text"]
        paper_type = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperType + " SpiceText[visible=true]")["text"]
        paper_tray = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_paperTray + " SpiceText[visible=true]")["text"]
        expected_string = paper_size+", "+paper_type+", "+paper_tray
        assert  get_paper_selection_string == expected_string
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
 
    finally:
        spice.goto_homescreen()     
   