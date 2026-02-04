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
    +purpose: Test booklet format left edge settings in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_booklet_format_on
    +test:
        +title:test_copy_ews_copy_setting_booklet_format_on
        +guid:c43db53b-8398-43d9-bd4e-c090cdbe066f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_booklet_format_on(ews, scan_emulation):
    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 8)
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["bookletFormat"] = "leftEdge"
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = "twoUp"
        update_expected_settings["dest"]["print"]["plexMode"] = "duplex"
        update_expected_settings["dest"]["print"]["duplexBinding"] = "twoSidedLongEdge"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_booklet_format_on)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test booklet format on and borders on each page settings in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_booklet_borders_on_each_page
    +test:
        +title:test_copy_ews_copy_setting_booklet_borders_on_each_page
        +guid:c9233393-b6fd-45ce-8604-ea3337eee555
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletBordersOnEachPage

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_booklet_borders_on_each_page(ews, scan_emulation):
    logging.info("Load 8 pages in ADF")
    scan_emulation.media.load_media('ADF', 8)
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["bookletFormat"] = "leftEdge"
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] = "twoUp"
        update_expected_settings["dest"]["print"]["plexMode"] = "duplex"
        update_expected_settings["dest"]["print"]["duplexBinding"] = "twoSidedLongEdge"
        update_expected_settings["pipelineOptions"]["imageModifications"]["imageBorder"] = "defaultLineBorder"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        image_border_elements =  ews.driver.find_elements(By.ID, 'imageBorder')
        assert len(image_border_elements) == 0, "Expected one image border element, found {}".format(len(image_border_elements))
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_booklet_format_on)
        time.sleep(10)
        image_border_elements =  ews.driver.find_elements(By.ID, 'imageBorder')
        assert len(image_border_elements) == 2, "Expected one image border element, found {}".format(len(image_border_elements))
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_borders_on_each_page_on)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with booklet format option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:360
    +asset:Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_booklet_format_on
    +test:
        +title:test_copy_ews_quickset_booklet_format_on
        +guid:0ca86ab2-caa3-4c34-b8de-2948538ed6ed
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_booklet_format_on(job, ews, spice, net, cdm, udw, scan_emulation):
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
            copy_options = copy_option_combi34
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi34.copy()
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
        copy_job_app.verify_copy_booklet_format_selection_option(net, "booklet_format", "on")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode='duplex',
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
    +purpose:Create quick set with booklet format and borders option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:360
    +asset:Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_booklet_borders_on_each_page
    +test:
        +title:test_copy_ews_quickset_booklet_borders_on_each_page
        +guid:86ba1610-dbf5-4fa6-82bc-e99965a1ac39
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletBordersOnEachPage

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_booklet_borders_on_each_page(job, ews, spice, net, cdm, udw, scan_emulation):
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
            copy_options = copy_option_combi35
        else:
            # Create a copy of the dictionary and remove the unwanted key-value pair
            copy_options = copy_option_combi35.copy()
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
        copy_job_app.verify_copy_booklet_format_selection_option(net, "booklet_format", "on")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode='duplex',
            image_border='defaultLineBorder')
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()
