import logging
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test sides option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_sides_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_sides_option_constrained
        +guid:a37d12b2-6be7-42a4-8d6d-7c84f8f8907d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_sides_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_sides_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test scan mode option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_scan_mode_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_scan_mode_option_constrained
        +guid:27269cd3-4549-4217-aefb-28a2035aa652
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_scan_mode_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_scan_mode_str_id,net,True)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test color mode option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_color_mode_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_color_mode_option_constrained
        +guid:5f29cb0e-a47c-4225-bbdd-8843527332d0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_color_mode_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.scan_colorMode_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'        

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test paper selection option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_paper_selection_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_paper_selection_option_constrained
        +guid:9224b189-ff4d-448b-8d4b-5accbcee3d5c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_paper_selection_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_paperSelection_str_id,net,True)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'        
 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test booklet option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_booklet_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_booklet_option_constrained
        +guid:aba258d7-30e5-4112-91b0-321f9d2c79ba
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_booklet_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_booklet_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test paper tray option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_paper_tray_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_paper_tray_option_constrained
        +guid:c2cc76c7-dcda-4a87-9694-8e984edb7323
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_paper_tray_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()
    copy_job_app.check_copy_action_button_enabled()
    if spice.uisize == "S":
        copy_job_app.goto_main_panel_from_preview()
    copy_job_app.goto_paper_source()    
    copy_job_app.validate_constrained_message_on_settings_option(net,CopyAppWorkflowObjectIds.copy_trays_str_id)    
    logging.info("Back to copy screen")
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test paper content type option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_content_type_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_content_type_option_constrained
        +guid:4ab745a4-9f03-4f45-8959-3f200a5cde0e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_content_type_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.scan_contentType_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
       
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test pages per sheet option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_pages_per_sheet_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_pages_per_sheet_option_constrained
        +guid:1425280e-9221-448c-bcab-c526bcc00e08
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_pages_per_sheet_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_pagesPerSheet_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test contrast option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_contrast_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_contrast_option_constrained
        +guid:515a845f-19a9-48b1-b81b-0bc6e7270221
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_contrast_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_slider_option_is_constrained(CopyAppWorkflowObjectIds.copy_contrast_str_id)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test output scale option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_output_scale_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_output_scale_option_constrained
        +guid:2519f4d9-e4a0-4958-865e-5f38ce9a31c8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_output_scale_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_resize_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test output bin option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_output_bin_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_output_bin_option_constrained
        +guid:ebd43692-2938-4982-8b75-a8197d1f15b9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & ProductSpecSupported=Finisher
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_output_bin_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_output_bin_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test sharpness option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_sharpness_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_sharpness_option_constrained
        +guid:1eca4652-80a0-4511-8cdb-caa8cbe1a5cf
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_sharpness_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

        logging.info("Load page in ADF")
        scan_emulation.media.load_media('ADF', 1)

        logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
        job.bookmark_jobs()
        logging.info("Go to copy screen")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.click_on_preview_button_in_preview_panel()
        copy_job_app.validate_preview_in_preview_panel()        
        copy_job_app.goto_copy_options_list_from_preview()
        copy_job_app.verify_slider_option_is_constrained(CopyAppWorkflowObjectIds.copy_sharpness_str_id)
        spice.goto_homescreen()
        spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

        job.wait_for_no_active_jobs()
        new_jobs = job.get_newjobs()
        assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test content orientation option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_content_orientation_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_content_orientation_option_constrained
        +guid:679c637c-71c0-41ba-b0f9-b0107271cd7e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_content_orientation_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):
    
    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_content_orientation_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test lighter/darker option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_lighter_darker_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_lighter_darker_option_constrained
        +guid:7a7fbe6a-24a4-466e-8d02-f64a05b7f009
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_lighter_darker_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):
    
    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel() 
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_slider_option_is_constrained(CopyAppWorkflowObjectIds.scan_lighterDarker_str_id)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test background cleanup option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_background_cleanup_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_background_cleanup_option_constrained
        +guid:488dd457-e948-43fd-8379-e3490e317bde
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_background_cleanup_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_slider_option_is_constrained(CopyAppWorkflowObjectIds.copy_background_cleanup_str_id)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test fold option constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_fold_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_fold_option_constrained
        +guid:11b5a2c0-20fa-45b6-9243-f50861f1fa9d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & ProductSpecSupported=Finisher
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_fold_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_fold_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test automatically straighten constrainted on preview job started
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-240518
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_when_preview_started_auto_straighten_option_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_when_preview_started_auto_straighten_option_constrained
        +guid:3939ef05-cdea-4032-9d92-0b9bbb4047f0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_preview_started_auto_straighten_option_constrained(scan_emulation, job, spice, net, setup_teardown_with_copy_job):

    logging.info("Load page in ADF")
    scan_emulation.media.load_media('ADF', 1)

    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.click_on_preview_button_in_preview_panel()
    copy_job_app.validate_preview_in_preview_panel()        
    copy_job_app.goto_copy_options_list_from_preview()
    copy_job_app.verify_copy_settings_option_constrained(CopyAppWorkflowObjectIds.copy_automatically_straighten_str_id,net)
    spice.goto_homescreen()
    spice.copy_ui().click_on_cancel_job_warning_prompt(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'        