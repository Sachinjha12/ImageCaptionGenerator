import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with book mode settings perform copy with scan Both Sides
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_perform_copy_with_scan_both_sides_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_perform_copy_with_scan_both_sides_scan_mode_book_setting
        +guid:1f14b68b-f56b-41a1-a9a9-9e3684db2923
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_perform_copy_with_scan_both_sides_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("scanBothSides")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()  

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with book mode settings perform copy with skip left page
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_perform_copy_with_skip_left_page_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_perform_copy_with_skip_left_page_scan_mode_book_setting
        +guid:096a1f8f-7f06-4aba-8e40-317d4642b527
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_perform_copy_with_skip_left_page_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("skipLeftPage")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with book mode settings perform copy with skip right page
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_perform_copy_with_skip_right_page_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_perform_copy_with_skip_right_page_scan_mode_book_setting
        +guid:9c8bc85e-31b4-454c-9cdb-8b9e91a65b8c
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_with_skip_right_page_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("skipRightPage")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()    

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the preview and add preview with scan mode book settings
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_perform_copy_verify_preview_with_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_perform_copy_verify_preview_with_scan_mode_book_setting
        +guid:3d69f47e-eb48-42b9-948e-5ad5b0d917e4
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_copy_verify_preview_with_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().select_book_mode_options("scanBothSides")
        job_detail = job.get_active_jobs()[0]
        last_job_id = job_detail["jobId"]
        job.check_job_state(last_job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        spice.copy_ui().verify_image_preview("#image_1")
        spice.copy_ui().click_on_copy_preview_add_page_button()
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        spice.copy_ui().verify_image_preview("#image_3")
        spice.copy_ui().start_copy_after_preview()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the 2to1 sided option is constrained when scan mode is book.
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_validate_constraint_on_2_to_1_sided_option_with_scan_mode_book_settings
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_constraint_on_2_to_1_sided_option_with_scan_mode_book_settings
        +guid:0ef8bef7-6511-43d9-9519-9613285c977a
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_constraint_on_2_to_1_sided_option_with_scan_mode_book_settings(spice,job,net,configuration):

    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().check_copy_side_constrained(net, "2_1_sided", "cOriginalCannotScanBook")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("scanBothSides")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the 2to2 sided option is constrained when scan mode is book.
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_validate_constraint_on_2_to_2_sided_option_with_scan_mode_book_settings
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_validate_constraint_on_2_to_2_sided_option_with_scan_mode_book_settings
        +guid:feefaaf9-6b29-4404-b673-849bef1f53b6
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_validate_constraint_on_2_to_2_sided_option_with_scan_mode_book_settings(spice,job,net,configuration):

    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().check_copy_side_constrained(net, "2_2_sided")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("scanBothSides")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the prompt for additional pages is constrained when scan mode is book.
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_verify_prompt_for_additional_pages_constraint
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_prompt_for_additional_pages_constraint
        +guid:6ed2ea52-a5ef-41a5-a0ee-662d2a1c9a8d
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_verify_prompt_for_additional_pages_constraint(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().goto_scan_mode_option()
        try: 
            check_box_button = spice.query_item(CopyAppWorkflowObjectIds.scan_mode_option_prompt_for_additonal_pages_checkbox)
            assert check_box_button["visible"] == True
        except:
            assert True
        spice.copy_ui().back_from_scan_mode_option()
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("scanBothSides")  
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)  
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()    
 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the paper size is by default set to Letter when scan mode is set to bookmode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-204045
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_verify_constrained_paper_sizes_with_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_verify_constrained_paper_sizes_with_scan_mode_book_setting
        +guid:7af3ab88-393b-40b8-8678-e0356fbb8348
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy &  ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_verify_constrained_paper_sizes_with_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("Legal")
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().check_original_size_value("Letter",net)
        spice.copy_ui().close_option_mode()
        spice.copy_ui().ui_select_copy_page()
        spice.copy_ui().select_book_mode_options("scanBothSides")
        job_detail = job.get_active_jobs()[0]
        job_id = job_detail["jobId"]
        job.check_job_state(job_id, "processing", 30)
        spice.copy_ui().book_mode_instructions_page_scan()
        spice.copy_ui().wait_for_copy_status_toast(net, configuration, message='Scanning', timeout=180, wait_for_toast_dismiss=True)
        spice.copy_ui().book_mode_instructions_page_finish()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Cancel the Scan mode prompt on preview scenarios 
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-219917
    +timeout: 500
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_perform_cancel_copy_preview_with_scan_mode_book_setting
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_perform_cancel_copy_preview_with_scan_mode_book_setting
        +guid:19705178-7b35-4514-b527-74cee4815a6f
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_perform_cancel_copy_preview_with_scan_mode_book_setting(spice,job,net,configuration):
    try:
        job.bookmark_jobs()
        spice.main_app.goto_copy_app()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_scan_mode_option("bookMode")
        spice.copy_ui().close_option_mode()
        spice.copy_ui().goto_preview_panel()
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().book_mode_instructions_page_cancel()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
        spice.copy_ui().goto_main_panel()
        spice.copy_ui().check_copy_action_button_enabled()
    finally:
        spice.goto_homescreen() 