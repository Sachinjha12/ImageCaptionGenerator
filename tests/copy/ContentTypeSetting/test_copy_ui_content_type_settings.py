import logging
import time
from dunetuf.copy.copy import *



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that copy options in the detailed options menu is working properly
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-148225
    +timeout:500
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_widget_change_detailed_options
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_widget_change_detailed_options
        +guid:2d304478-e32b-4fb6-a639-a8fdf61e4f8e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & UIComponent=CopyWidget & Widget=Settings
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_widget_change_detailed_options(spice, cdm, udw, tcl, job, copy, net, setup_teardown_print_device):

    # HomeScreen
    home = spice.main_app.get_home()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)
    spice.validate_app(home, False)

    # Start Copy 
    spice.copy_ui().launch_copyapp_from_widget_more_options()

    # Size of the FrontPanel
    ui_size = udw.mainUiApp.ControlPanel.getBreakPoint()

    #App must be open for all products
    spice.copy_ui().wait_for_copy_landing_view_from_widget_or_one_touch_quickset()

    if ui_size in ["XL"]:

        #Preview and summaryze setings shown
        assert not spice.copy_ui().is_landing_expanded(spice)

        #Check Qs are shown
        assert spice.copy_ui().are_quicksets_visible(spice)

        # Modify some options
        SETTINGS_TO_CHANGE={'originalPaperType': 'translucent','resolution':'600Dpi'}
        spice.copy_ui().goto_select_setting_with_payload_and_back_landing_view(udw, net, SETTINGS_TO_CHANGE)

    # go back to mainApp to check that value has remained after entering the copyApp:
    spice.copy_app.goto_home()

    spice.validate_app(home, True)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting Content Type as Mixed
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_content_type_mixed
    +test:
        +title: test_copy_ui_adf_landingpage_content_type_mixed
        +guid: c1c0f55c-a5e2-4c3d-8183-5fc76c673999
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScanContentType=Mixed & ScannerInput=AutomaticDocumentFeeder
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:500
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_content_type_mixed(cdm, spice, job, udw, net,scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'contentType': 'Mixed'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting Content Type as Text
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_content_type_text
    +test:
        +title: test_copy_ui_adf_menupage_content_type_text
        +guid: 0742ae7b-b728-4c22-8483-97bac666bc5a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanContentType=Text
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:500
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_content_type_text(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'contentType': 'Text'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting Content Type as photograph
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_content_type_photograph
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_content_type_photograph
        +guid: f1da5eff-0690-48f3-a29c-681fb491952e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanContentType=Photograph & Widget=Settings  & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_content_type_photograph(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'contentType': 'Photograph'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting Content Type as lines
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_mdf_widget_content_type_lines
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_mdf_widget_content_type_lines
        +guid: 2b3ea7ac-707c-4e11-9f4e-16cb911fc489
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScanContentType=Lines & ScannerInput=ManualFeeder  & Widget=Settings  & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_widget_content_type_lines(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'contentType': 'Lines'
            }
        loadmedia = 'MDF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting Content Type as image
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_mdf_menupage_content_type_image
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_mdf_menupage_content_type_image
        +guid: e0900a43-b0ea-4c46-b061-054dd7366d7b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScanContentType=Image & ScannerInput=ManualFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_mdf_menupage_content_type_image(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'contentType': 'Image'
            }
        loadmedia = 'MDF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

