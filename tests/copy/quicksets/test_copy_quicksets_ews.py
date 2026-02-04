import logging
import copy
from dunetuf.copy.copy import *
from tests.send.quicksets.email.email_combination import *
from tests.send.quicksets.scantousb.usb_combination import *
from tests.send.quicksets.folder.network_folder_combination import *
from tests.send.quicksets.quicksets_common import *
from tests.copy.quicksets.copy_common import verify_create_copy_quick_set_from_ews,\
                                             check_with_cdm_on_ews_quick_sets_copy, check_with_cdm_on_ews_quick_sets_copy_custom,\
                                             check_quickset_order_by_quick_set_name, check_quickset_order_by_quick_set_type,\
                                             check_quickset_order_by_start_option, expected_cdm_for_copy_default_from_actual_cdm
from tests.copy.quicksets.copy_combination import *
from tests.send.quicksets.quicksets_common import get_local_time

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with default settings and start automatically when select
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_startoption_from_home
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_startoption_from_home
        +guid:162ef60a-0bb8-4da7-9e50-0032ec2adca5
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & EWS=Quicksets

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_quickset_ews_add_defaultsettings_startoption_from_home(ews):
    try:
        expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with min outputrange
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_outputrange_custom_min_range
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_outputrange_custom_min_range
        +guid:f1c7ec1d-1749-43a6-9845-32a58a41d8e7
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScanOriginalSides=1-sided & EWS=Quicksets & ScanColorMode=Automatic

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_outputrange_custom_min_range(ews):
    #test disabled untill DUNE-145073 is fixed
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["xScalePercent"] = 25
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["yScalePercent"] = 25
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "custom"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.output_scale] = CopyOptions.CopyOutputScale.custom
        update_copy_option[CopyOptionsKey.precise_scaling_amount] = 25
        
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with max outputrange
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_outputrange_custom_max_range
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_outputrange_custom_max_range
        +guid:683901e9-9041-4a17-8aa6-509900cc0b67
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScanOriginalSides=1-sided & EWS=Quicksets & ScanColorMode=Automatic

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_outputrange_custom_max_range(ews):
    #test disabled untill DUNE-145073 is fixed
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["xScalePercent"] = 400
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["yScalePercent"] = 400
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "custom"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.output_scale] = CopyOptions.CopyOutputScale.custom
        update_copy_option[CopyOptionsKey.precise_scaling_amount] = 400
        
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with 100 outputrange
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:150
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_outputrange_custom_100
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_outputrange_custom_100
        +guid:be3074c5-e5f5-4214-8905-e3023dc059c5
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScanOriginalSides=1-sided & EWS=Quicksets & ScanColorMode=Automatic

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_outputrange_custom_100(ews):
    #test disabled untill DUNE-145073 is fixed
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["xScalePercent"] = 100
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["yScalePercent"] = 100
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "custom"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.output_scale] = CopyOptions.CopyOutputScale.custom
        update_copy_option[CopyOptionsKey.precise_scaling_amount] = 100
        
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with SEF paper option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_quickset_ews_paper_SEF_option
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_quickset_ews_paper_SEF_option
        +guid:4224b993-1a7b-4e92-84f2-9a5ee91cbf66
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceClass=MFP & PrintEngineFormat=A3 & MediaInputInstalled=Tray2
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_ews_paper_SEF_option(job, tray, ews, spice, net, cdm, udw):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    try:
        tray.unload_media('all')
        if tray.is_size_supported('com.hp.ext.mediaSize.iso_a4_210x297mm.rotated', 'tray-1'):
            tray.configure_tray('tray-1', 'com.hp.ext.mediaSize.iso_a4_210x297mm.rotated', 'stationery')
            tray.load_media('tray-1')

        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi25
        )
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for Original Size and Paper Size")
        copy_job_app.verify_copy_mediasize_selected_option(net, "original", "A4_SEF")
        copy_job_app.verify_copy_mediasize_selected_option(net, "paper", "A4_SEF")

        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size= "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated",
            paper_size = "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated")
        time.sleep(20)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()
        tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with match original paper option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143686
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_papersize_match_original
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_papersize_match_original
        +guid:359164ee-b1fa-438e-a690-08498b3931ac
        +dut:
            +type:Simulator
            +configuration: DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_papersize_match_original(ews):
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["dest"]["print"]["mediaSize"] = "any"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "none"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.paper_size] = CopyOptions.CopyPaperSize.Match_Original
        
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with custom paper option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143690
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_papersize_custom
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_papersize_custom
        +guid:8b86023e-8899-4ed4-be40-e6649f370714
        +dut:
            +type:Simulator
            +configuration: DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_papersize_custom(ews):
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["dest"]["print"]["mediaSize"] = "custom"
        #a4 210x297mm
        update_expected_cdm["settings_info"]["dest"]["print"]["customMediaXFeedDimension"] = 80000.0
        update_expected_cdm["settings_info"]["dest"]["print"]["customMediaYFeedDimension"] = 110000.0
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "none"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.paper_size] = CopyOptions.CopyPaperSize.custom

        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        if(ews.driver.find_element(By.ID, "displayUnitOfMeasure").text!="Inches"):
            update_copy_option[CopyOptionsKey.unit_of_measurement] = CopyOptions.UnitOfMeasure.inches

        update_copy_option[CopyOptionsKey.custom_media_x_feed_dimension] = str(8.00)
        qs.edit_copy_setting(update_copy_option)
        update_copy_option[CopyOptionsKey.custom_media_y_feed_dimension] = str(11.00)
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy_custom(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with manual feed tray option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143706
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_tray_manual_feed
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_tray_manual_feed
        +guid:8bcdfe8d-af77-4d26-8a11-9663f077e4fa
        +dut:
            +type:Simulator
            +configuration: DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_tray_manual_feed(ews):  
    try:
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        update_expected_cdm["settings_info"]["dest"]["print"]["mediaSource"] = "manual"
        update_expected_cdm["settings_info"]["src"]["scan"]["mediaSize"] = "na_letter_8.5x11in"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleToFitEnabled"] = "false"
        update_expected_cdm["settings_info"]["pipelineOptions"]["scaling"]["scaleSelection"] = "none"

        update_copy_option = copy.deepcopy(copy_option_default)
        update_copy_option[CopyOptionsKey.paper_tray] = CopyOptions.CopyPaperTray.manual_feed
        update_copy_option[CopyOptionsKey.original_size] = CopyOptions.CopyOriginalSize.Letter_8_5x11_in_

        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        qs.edit_copy_setting(update_copy_option)

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        check_with_cdm_on_ews_quick_sets_copy(qs, copy_title_name, update_expected_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with mixed letter ledger original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_basic_mixed_letter_ledger
    +test:
        +title:test_copy_quickset_ews_basic_mixed_letter_ledger
        +guid:54ff9720-e57d-4788-8708-2829d9421154
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLedger & EWS=Quicksets
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_basic_mixed_letter_ledger(job, ews, spice, net, cdm, udw, scan_emulation):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi37
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi37.copy()
            del copy_options[CopyOptionsKey.color]
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for original size")
        copy_job_app.check_original_size_value("MIXED_LETTER_LEDGER", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-letter-ledger")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with mixed letter legal original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_basic_mixed_letter_legal
    +test:
        +title:test_copy_quickset_ews_basic_mixed_letter_legal
        +guid:6c1d5c4d-531f-43dd-a627-b85df3e47034
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLegal & EWS=Quicksets
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_basic_mixed_letter_legal(job, ews, spice, net, cdm, udw, scan_emulation):
    try:
        logging.info("Load 4 pages in ADF")
        scan_emulation.media.load_media('ADF', 4)
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi38
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair if it exists
            copy_options = copy_option_combi38.copy()
            if CopyOptionsKey.color in copy_options:  # Added line
                del copy_options[CopyOptionsKey.color]  # Added line
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for original size")
        copy_job_app.check_original_size_value("MIXED_LETTER_LEGAL", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-letter-legal")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with mixed A4 A3 original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_basic_mixed_a4_a3
    +test:
        +title:test_copy_quickset_ews_basic_mixed_a4_a3
        +guid:17cf5686-66fc-4854-b680-71e88e921520
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedA4A3 & EWS=Quicksets
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_basic_mixed_a4_a3(job, ews, spice, net, cdm, udw, scan_emulation):
    try:
        logging.info("Load 4 pages in ADF")
        scan_emulation.media.load_media('ADF', 4)
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi39
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi39.copy()
            del copy_options[CopyOptionsKey.color]
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for staple")
        copy_job_app.check_original_size_value("MIXED_A4_A3", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-a4-a3")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with flatbed mixed letter ledger original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_flatbed_mixed_letter_ledger
    +test:
        +title:test_copy_quickset_ews_flatbed_mixed_letter_ledger
        +guid:3d30396b-2be7-4061-a602-644fc888e90a
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLedger & EWS=Quicksets
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_flatbed_mixed_letter_ledger(job, ews, spice, net, cdm, udw, scan_emulation, configuration):
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi37
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi37.copy()
            del copy_options[CopyOptionsKey.color]
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for original size")
        copy_job_app.check_original_size_value("MIXED_LETTER_LEDGER", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.load_media('Flatbed', 4)
        logging.info("Start a copy job")
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded)
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-letter-ledger")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF')
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with flatbed mixed letter legal original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_flatbed_mixed_letter_legal
    +test:
        +title:test_copy_quickset_ews_flatbed_mixed_letter_legal
        +guid:ab1b287a-2857-4347-9945-318cc8c7bca5
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLegal & EWS=Quicksets & FlatbedMediaSize=MixedLetterLegal
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_flatbed_mixed_letter_legal(job, ews, spice, net, cdm, udw, scan_emulation, configuration):
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi38
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi38.copy()
            del copy_options[CopyOptionsKey.color]
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for original size")
        copy_job_app.check_original_size_value("MIXED_LETTER_LEGAL", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.load_media('Flatbed', 4)
        logging.info("Start a copy job")
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded)
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-letter-legal")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF')
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with flatbed mixed A4 A3 original size option
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-226051
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_quickset_ews_flatbed_mixed_a4_a3
    +test:
        +title:test_copy_quickset_ews_flatbed_mixed_a4_a3
        +guid:b8d875b4-c2a7-414f-89db-5910dba5eb4e
        +dut:
            +type: Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedA4A3 & EWS=Quicksets
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator   
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_flatbed_mixed_a4_a3(job, ews, spice, net, cdm, udw, scan_emulation, configuration):
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi39
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi39.copy()
            del copy_options[CopyOptionsKey.color]
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_options
        )

        logging.info("Check quickset in EWS")
        short_cut_id = qs.csc.get_shortcut_id(copy_quicksets_name_list[0])
        qs_index = qs.find_quick_set_by_title(copy_quicksets_name_list[0])
        assert qs_index != -1, "Quickset not found!"

        logging.info("Close the current browser")
        ews.close_browser()

        logging.info("Select quickset in Copy UI")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_quickset_view()
        copy_job_app.select_copy_quickset("#" + short_cut_id)
        copy_job_app.goto_copy_options_list()

        logging.info("Verify the value displayed for staple")
        copy_job_app.check_original_size_value("MIXED_A4_A3", net)
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Load 4 pages in Flatbed")
        scan_emulation.media.load_media('Flatbed', 4)
        logging.info("Start a copy job")
        adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
        copy_job_app.start_copy(familyname = configuration.familyname, adfLoaded = adfLoaded)
        Copy(cdm, udw).validate_settings_used_in_copy(
            original_size="com.hp.ext.mediaSize.mixed-a4-a3")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        scan_emulation.media.load_media('ADF')
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()