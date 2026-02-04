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
    +purpose: Test blank page suppression selection settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24421
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_default_copy_setting_blank_page_suppression
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_default_copy_setting_blank_page_suppression
        +guid:4b559c16-2fec-48b0-a4e0-7288d0bf5fff
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & DigitalStorageType=HardDisk & ScannerInput=AutomaticDocumentFeeder

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_setting_blank_page_suppression(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["blankPageSuppressionEnabled"] = "true"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set blank page suppression values as true")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_blankPageSuppression_enabled)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with blank page suppression option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24421
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_quickset_blank_page_suppression
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_quickset_blank_page_suppression
        +guid:48ee009e-122b-4a4a-bbe7-4b68af89e455
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & DigitalStorageType=HardDisk & ScannerInput=AutomaticDocumentFeeder
            
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_blank_page_suppression(job, ews, spice, net, cdm, udw):  
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        if ews.cdm.device_feature_cdm.is_color_supported()== False:
            copy_option_combi26.pop("color")

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi26
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

        logging.info("Verify the value displayed for blank page suppression")
        copy_job_app.verify_copy_settings_selected_option(net, "blank_page_suppression", "on")

        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(blank_page_suppression= "true")
        time.sleep(5)
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()
