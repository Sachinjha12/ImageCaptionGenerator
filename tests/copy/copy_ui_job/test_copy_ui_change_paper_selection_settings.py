import logging
import pytest
import time
from typing import ClassVar

from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper


def goto_paper_selection_paper_size(self, spice, to_select_item):
    self.goto_copy()
    self.goto_copy_options_list()
    self.homemenu.menu_navigation(spice, 
                                  CopyAppWorkflowObjectIds.view_copySettingsView, 
                                  CopyAppWorkflowObjectIds.list_copySettings_paperSelection, 
                                  select_option = False, 
                                  scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
    self.go_to_paper_selection()
    self.goto_copy_paper_size_screen()
    time.sleep(10)

    self.workflow_common_operations.goto_item(to_select_item, 
        CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
        scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar,
        select_option=False) 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test paper selection match original size values in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_check_paper_selection_match_size_value_test
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_check_paper_selection_match_size_value_test
        +guid:083512e0-9436-4224-aa03-d4d425770a65
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_check_paper_selection_match_size_value_test(spice):
    try:
        # set paper size
        copy_job_app = spice.copy_ui()
        to_select_item = CopyAppWorkflowObjectIds.row_media_size_any
        goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
        custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
        custom_button.mouse_click()

        # check changed paper size
        paper_size = spice.wait_for("#copy_mediaSizeSettingsTextImage_2infoBlockRow SpiceText[visible=true]")["text"]
        paper_size_ref = "Match Original Size"
        assert  paper_size == paper_size_ref, "Not matched" 

        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test paper selection custom size values in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:1100
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_check_paper_selection_custom_size_value_test
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_check_paper_selection_custom_size_value_test
        +guid:524dbe41-e92a-47ad-b628-f9e96747012a
        +dut:
            +type:Emulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_check_paper_selection_custom_size_value_test(spice, configuration):
    try:
        # set paper size
        copy_job_app = spice.copy_ui()
        to_select_item = CopyAppWorkflowObjectIds.row_media_size_custom
        
        goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
        custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
        custom_button.mouse_click()
        data_list = [
            {'unit': 'mm', 'value_x' : 200, 'value_y' : 200},
            {'unit': 'mm', 'value_x' : 10, 'value_y' : 10},
            {'unit': 'mm', 'value_x' : 500, 'value_y' : 500}
        ]
        logging.info("Set and verify value(unit, x, y)")
        for data in data_list:
            unit = data['unit']
            value_x = data['value_x']
            value_y = data['value_y']
            # set inch, x, y values
            logging.info("set inch, x, y values")
            copy_job_app.set_copy_custom_size_value(unit, value_x, value_y, configuration)
            # initialize x, v values

            if configuration.productname in ["camden", "busch"] :
                x_range = (76, 216)
                y_range = (127, 356)
            else:
                x_range = (98, 320)
                y_range = (140, 457)

            value_x = "{:d}".format(round(max(min(value_x, x_range[1]), x_range[0]),0))
            value_y = "{:d}".format(round(max(min(value_y, y_range[1]), y_range[0]),0))

            # verify changed values_1
            result = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.row_media_size_custom + " #infoBlockRow" + " " + CopyAppWorkflowObjectIds.text_view, timeout=9.0)['text']
            ref = f"({value_x}x{value_y} mm)"
            assert result == ref, "Not matched"
            # verify changed values_2
            copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize + " " + CopyAppWorkflowObjectIds.button_back, timeout=9.0).mouse_click()
            time.sleep(2)
            paper_size = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.view_copySettings_paperSize + " " + CopyAppWorkflowObjectIds.text_view)["text"]
            print(paper_size) #Custom
            assert paper_size == 'Custom', 'Not matched'
            # go to paper size (custom size)
            copy_job_app.goto_copy_paper_size_screen()
            time.sleep(10)
            copy_job_app.workflow_common_operations.goto_item(to_select_item, 
                CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
                scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar,
                select_option=False) 
            custom_button.mouse_click()
        
        btn = copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view + " " + CopyAppWorkflowObjectIds.button_back, timeout=9.0)
        time.sleep(2)
        btn.mouse_click()
        copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize +" " + CopyAppWorkflowObjectIds.button_back, timeout=9.0).mouse_click()
        time.sleep(2)
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()

    finally:
        spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test paper selection custom size values(inch) in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-168377
    +timeout:1100
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_check_paper_selection_custom_size_value_inch_test
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_check_paper_selection_custom_size_value_inch_test
        +guid:0e820af9-c2e0-4cd7-a591-5c6433c8be65
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_check_paper_selection_custom_size_value_inch_test(spice, configuration):
    try:
        # set paper size
        copy_job_app = spice.copy_ui()
        to_select_item = CopyAppWorkflowObjectIds.row_media_size_custom
        
        goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
        custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
        custom_button.mouse_click()
        data_list = [
            {'unit': 'inch', 'value_x' : 7, 'value_y' : 7},
            {'unit': 'inch', 'value_x' : 1, 'value_y' : 1},
            {'unit': 'inch', 'value_x' : 22, 'value_y' : 22}
        ]
        logging.info("Set and verify value(unit, x, y)")
        for data in data_list:
            unit = data['unit']
            value_x_in = data['value_x']
            value_y_in = data['value_y']
            # set inch, x, y values
            logging.info("set inch, x, y values")
            copy_job_app.set_copy_custom_size_value(unit, value_x_in, value_y_in, configuration)
            # initialize x, v values
            value_x_mm = value_x_in * 25.4
            value_y_mm = value_y_in * 25.4

            if configuration.productname in ["camden", "busch"] :
                x_range = (76, 216)
                y_range = (127, 356)
            else:
                x_range = (98, 320)
                y_range = (140, 457)

            value_x_mm = str(int(round(max(min(value_x_mm, x_range[1]), x_range[0]),0)))
            value_y_mm = str(int(round(max(min(value_y_mm, y_range[1]), y_range[0]),0)))

            # verify changed values_1
            result = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.row_media_size_custom + " #infoBlockRow" + " " + CopyAppWorkflowObjectIds.text_view, timeout=9.0)['text']
            ref = f"({value_x_mm}x{value_y_mm} mm)"
            assert result == ref, "Not matched"
            # verify changed values_2
            copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize + " " + CopyAppWorkflowObjectIds.button_back, timeout=9.0).mouse_click()
            time.sleep(2)
            paper_size = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.view_copySettings_paperSize + " " + CopyAppWorkflowObjectIds.text_view)["text"]
            print(paper_size) #Custom
            assert paper_size == 'Custom', 'Not matched'
            # go to paper size (custom size)
            copy_job_app.goto_copy_paper_size_screen()
            time.sleep(10)
            copy_job_app.workflow_common_operations.goto_item(to_select_item, 
                CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
                scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar,
                select_option=False) 
            custom_button.mouse_click()
        
        btn = copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.copy_settings_paper_selection_media_size_custom_size_view + " " + CopyAppWorkflowObjectIds.button_back, timeout=9.0)
        time.sleep(2)
        btn.mouse_click()
        copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize +" " + CopyAppWorkflowObjectIds.button_back, timeout=9.0).mouse_click()
        time.sleep(2)
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test done button in custom size view
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-168386
    +timeout:400
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_check_done_button_custom_size
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_check_done_button_custom_size
        +guid:3e840301-887d-42df-b2ef-b40b157d8688
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_check_done_button_custom_size(spice, configuration):
    try:
        # set paper size
        copy_job_app = spice.copy_ui()
        to_select_item = CopyAppWorkflowObjectIds.row_media_size_custom
        goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
        custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
        custom_button.mouse_click()
        data_list = [
            {'unit': 'mm', 'value_x' : 200, 'value_y' : 200},
            # {'unit': 'inch', 'value_x' : 11.8, 'value_y' : 11.8},
        ]
        logging.info("Set and verify value(unit, x, y)")
        for data in data_list:
            unit = data['unit']
            value_x = data['value_x']
            value_y = data['value_y']

            # set inch, x, y values
            logging.info("set inch, x, y values")
            copy_job_app.set_copy_custom_size_value(unit, value_x, value_y, configuration, "done")
            
            # verify changed values_1
            result = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.row_media_size_custom + " #infoBlockRow" + " " + CopyAppWorkflowObjectIds.text_view, timeout=9.0)['text']
            ref = f"({value_x}x{value_y} {unit})"
            assert result == ref, "Not matched"

            # verify changed values_2
            copy_job_app.spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize + " " + CopyAppWorkflowObjectIds.button_back, timeout=9.0).mouse_click()
            time.sleep(2)
            paper_size = copy_job_app.spice.wait_for( CopyAppWorkflowObjectIds.view_copySettings_paperSize + " " + CopyAppWorkflowObjectIds.text_view)["text"]
            print(paper_size) #Custom
            assert paper_size == 'Custom', 'Not matched'

        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test tray values in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_check_paper_selection_tray_value_test
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_check_paper_selection_tray_value_test
        +guid:d2767c6d-b969-4982-9a69-2bef6ca72545
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_check_paper_selection_tray_value_test(spice):
    try:
        # set paper tray
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.homemenu.menu_navigation(spice, 
                                            CopyAppWorkflowObjectIds.view_copySettingsView, 
                                            CopyAppWorkflowObjectIds.list_copySettings_paperSelection, 
                                            select_option = False, 
                                            scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        copy_job_app.go_to_paper_selection()
        copy_job_app.select_paper_tray_option("Manual feed") # "Manual feed"

        # check changed paper tray
        paper_tray = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_paperTray + " SpiceText[visible=true]")["text"]
        paper_tray_ref = "Manual Feed" # "Manual feed"
        assert  paper_tray == paper_tray_ref, "Not matched"

        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
    finally:
        spice.goto_homescreen()
