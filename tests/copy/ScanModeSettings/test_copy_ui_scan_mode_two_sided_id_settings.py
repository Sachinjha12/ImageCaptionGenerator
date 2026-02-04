import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with 2-Sided Id type and promptforScanBothSides pages set to true and Load media Flatbed
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true
        +guid:e83404f5-0d20-464d-9b02-7d9a11b3c67e
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().handle_two_sided_id_prompt(net, "front","scan")
        time.sleep(1)
        spice.copy_ui().handle_two_sided_id_prompt(net, "back", "done")

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with 2-Sided Id type, cancel Job From ScanDuplex Alert Prompt
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_cancel_job_from_scanDuplex_alert_prompt
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_cancel_job_from_scanDuplex_alert_prompt
        +guid:e2b397f6-641a-47ef-9e6a-254c061e5959
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_cancel_job_from_scanDuplex_alert_prompt(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().handle_two_sided_id_prompt(net, "front","scan")
        time.sleep(1)
        spice.copy_ui().handle_two_sided_id_prompt(net, "back", "cancel")

        yes_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_flatbed_cancel_job_prompt_yes_button)
        yes_button.mouse_click()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with 2-Sided Id type and promptforScanBothSides pages set to false
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_false
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_false
        +guid:3b24ef62-ec24-4350-bb4e-3043bc2977a8
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_false(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': False
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().handle_two_sided_id_prompt(net, "back", "done")

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate constrained on bookletMode setting when ScanMode setting in copy options is 2-Sided Id
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_constrained_on_booklet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_constrained_on_booklet
        +guid:27c61fab-17b0-4e74-9e46-f45a3ef15939
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_constrained_on_booklet(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_booklet_constrained(net, "cBookletOptionChanged")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate constrained on Pages per sheet setting when ScanMode setting in copy options is 2-Sided Id
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_constrained_on_pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_constrained_on_pages_per_sheet
        +guid:c1343a9c-2a2a-4d65-817b-b79cb8ba10b6
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_constrained_on_pages_per_sheet(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_pages_per_sheet_constrained(udw, net , constrained_message = "cFeatureCurrentNotAvailable")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")  


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate constrained on Content Orientation setting when ScanMode setting in copy options is 2-Sided Id
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_constrained_on_content_orientation
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_constrained_on_content_orientation
        +guid:547b4c82-daf4-41f0-af8b-7234aa50563a
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_constrained_on_content_orientation(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_content_orientation_constrained(net, "cContentOrientationOption")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate constrained on Original Sides setting when ScanMode setting in copy options is 2-Sided Id
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_constrained_on_original_sides
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_constrained_on_original_sides
        +guid:617f6e76-4306-430e-b331-e453552cc914
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_constrained_on_original_sides(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().check_copy_side_constrained(net, "1_1_sided", "cScanOriginalSides")
        spice.copy_ui().check_copy_side_constrained(net, "1_2_sided", "cScanOriginalSides")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the Copy Job With Preview and 2-sided Id ScanMode options and Prompt for Additional Pages set to true
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_preview_job_with_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_preview_job_with_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true
        +guid:46ff831d-af14-4fee-a0f1-148f72a50b23
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_preview_job_with_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true(net, job, spice, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("idCard", True)
        spice.copy_ui().close_option_mode()
        spice.copy_ui().goto_preview_panel()
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        
        spice.copy_ui().handle_two_sided_id_prompt(net, "front","scan")
        time.sleep(1)
        spice.copy_ui().handle_two_sided_id_prompt(net, "back", "done")

        spice.copy_ui().verify_image_preview("#image_0")
        spice.copy_ui().click_on_main_action_button_in_main_panel()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the Copy Job With  2-sided Id ScanMode options and Prompt for Additional Pages set to true and Click on Front Side Done
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208125
    +timeout: 180
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true_front_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true_front_done
        +guid:c79ff82e-c82b-4f64-8113-a1078b6ca34f
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScanMode=2SidedID

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_two_sided_id_scanMode_and_prompt_for_scan_both_sides_true_front_done(net, job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'scan_scanMode': 'idCard',
            'checkBox_for_scan_mode_prompt': True
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        spice.copy_ui().handle_two_sided_id_prompt(net, "front","done")

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "failed"}],time_out=120)
    
    finally:
        spice.goto_homescreen()
        udw.mainApp.ScanMedia.loadMedia("ADF")
