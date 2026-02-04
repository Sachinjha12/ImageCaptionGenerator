import logging
import copy
from dunetuf.copy.copy import Copy
from dunetuf.job.job import Job
from tests.copy.ews.copy_default_settings.copy_ews_combination import *
from tests.send.quicksets.email.email_combination import *
from tests.send.quicksets.scantousb.usb_combination import *
from tests.send.quicksets.folder.network_folder_combination import *
from tests.send.quicksets.quicksets_common import *
from tests.copy.quicksets.copy_common import verify_create_copy_quick_set_from_ews, check_with_cdm_on_ews_quick_sets_copy,\
                                             check_quickset_order_by_quick_set_name, check_quickset_order_by_quick_set_type,\
                                             check_quickset_order_by_start_option, expected_cdm_for_copy_default_from_actual_cdm
from tests.copy.quicksets.copy_combination import *
from tests.send.quicksets.quicksets_common import get_local_time

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test pages per sheet 4up settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_4up_right_then_down
    +test:
        +title:test_copy_ews_copy_setting_4up_right_then_down
        +guid:af2badf2-d37e-47f4-b3c1-61a7298047c6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FourRightThenDownPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_4up_right_then_down(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = "fourUp"
        update_expected_settings["pipelineOptions"]["imageModifications"]["numberUpPresentationDirection"] = "toRightToBottom"
        update_expected_settings["pipelineOptions"]["imageModifications"]["imageBorder"] = "noBorder"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_pages_per_sheet_four_right_then_down)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test pages per sheet 4up settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_4up_down_then_right
    +test:
        +title:test_copy_ews_copy_setting_4up_down_then_right
        +guid:03ec036d-fc6c-4dee-ad3f-7562a5592bed
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FourDownThenRightPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_4up_down_then_right(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = "fourUp"
        update_expected_settings["pipelineOptions"]["imageModifications"]["numberUpPresentationDirection"] = "toBottomToRight"
        update_expected_settings["pipelineOptions"]["imageModifications"]["imageBorder"] = "noBorder"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_pages_per_sheet_four_down_then_right)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test pages per sheet 4up settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_4up_add_page_borders
    +test:
        +title:test_copy_ews_copy_setting_4up_add_page_borders
        +guid:3bfc4081-2111-442c-9695-ab0cdae2b0e7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=AddPageBordersPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_4up_add_page_borders(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = "fourUp"
        update_expected_settings["pipelineOptions"]["imageModifications"]["numberUpPresentationDirection"] = "toBottomToRight"
        update_expected_settings["pipelineOptions"]["imageModifications"]["imageBorder"] = "defaultLineBorder"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_pages_per_sheet_four_down_then_right)
        time.sleep(10)
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_add_page_borders_default_line_border)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
        
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with 4up option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:400
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_4up_right_then_down
    +test:
        +title:test_copy_ews_quickset_4up_right_then_down
        +guid:55bc58df-ad3e-4286-a2a2-538d8efe8c5f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FourRightThenDownPagesPerSheet

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_4up_right_then_down(job, ews, spice, net, cdm, udw):
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)

        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi30
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi30.copy()
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
        copy_job_app.verify_copy_settings_selected_option(net, "pages_per_sheet", "fourup_right_then_down")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toRightToBottom",
            image_border='noBorder')
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with 4up option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_4up_down_then_right
    +test:
        +title:test_copy_ews_quickset_4up_down_then_right
        +guid:79d94073-fa0a-454c-86da-426dadb0d9f8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=FourDownThenRightPagesPerSheet

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_4up_down_then_right(job, ews, spice, net, cdm, udw):
    
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)

        logging.info("Create copy quickset")
        if color_supported:
           copy_options = copy_option_combi31
        else:
        # Create a copy of the dictionary and remove the unwanted key-value pair
           copy_options = copy_option_combi31.copy()
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
        copy_job_app.verify_copy_settings_selected_option(net, "pages_per_sheet", "fourup_down_then_right")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toBottomToRight",
            image_border='noBorder')
        time.sleep(5)

        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with add page border option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_add_page_border
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_quickset_add_page_border
        +guid:62b60a1d-6161-4eb7-a002-2c7568d87800
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=AddPageBordersPagesPerSheet

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_add_page_border(job, ews, spice, net, cdm, udw):
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        color_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        logging.info("Create copy quickset")
        if color_supported:
            copy_options = copy_option_combi32
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi32.copy()
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
        copy_job_app.verify_copy_settings_selected_option(net, "pages_per_sheet", "fourup_right_then_down")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            pages_per_sheet='fourUp',
            numberUp_presentation_direction="toRightToBottom",
            image_border='defaultLineBorder')
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()
