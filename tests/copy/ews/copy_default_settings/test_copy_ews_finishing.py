import logging
import copy
from dunetuf.copy.copy import Copy
from dunetuf.job.job import Job
from selenium.webdriver.common.by import By
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
    +purpose: Test Staple settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_staple
    +test:
        +title:test_copy_ews_copy_setting_staple
        +guid:c09c5a6c-f2c7-4d1f-aeed-da489abd9880
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=Staple

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_staple(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["stapleOption"] = "leftTwoPoints"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set staple values as topRightOnePointAngled")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_staple_leftTwoPoints)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with staple option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_staple
    +test:
        +title:test_copy_ews_quickset_staple
        +guid:407ac081-ac69-4c71-b491-c443133aa5bd
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=Staple

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_staple(job, ews, spice, net, cdm, udw):  
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi27
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
        copy_job_app.verify_copy_settings_selected_option(net, "finisher_staple", "leftTwoPoints")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_staple= "leftTwoPoints")
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
    +purpose: Test Punch settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_punch
    +test:
        +title:test_copy_ews_copy_setting_punch
        +guid:4ca382b1-f5fa-4791-bec2-9ff64ff0bbee
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=HolePunch

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_setting_punch(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["punchOption"] = "rightTwoPointDin"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set punch values as rightTwoPointDin")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_punch_rightTwoPointDin)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with punch option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-142400
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_punch
    +test:
        +title:test_copy_ews_quickset_punch
        +guid:34f16c5d-716c-4cda-841c-8248cc1fa1cb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=HolePunch

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_punch(job, ews, spice, net, cdm, udw):  
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi28
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

        logging.info("Verify the value displayed for punch")
        copy_job_app.verify_copy_settings_selected_option(net, "finisher_punch", "rightTwoPointDin")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_punch= "rightTwoPointDin")
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
    +purpose: Test Fold settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184313
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_fold
    +test:
        +title:test_copy_ews_copy_setting_fold
        +guid:fc9b844d-6973-4ecb-b172-d0d12a8ef8c5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews_copy_setting_fold(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["foldOption"] = "vInwardTop"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set punch values as rightTwoPointDin")
        vFoldOption = ews.helper.wait_for_element_visible((By.ID, 'foldSelectorOption-nvOption-cVFold'))
        vFoldOption.click()

        time.sleep(5)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with fold option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184313
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_fold
    +test:
        +title:test_copy_ews_quickset_fold
        +guid:2b50779f-05e3-4d87-ba94-ce1c1d9bc763
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_fold(job, ews, spice, net, cdm, udw):  
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi33
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

        logging.info("Verify the value displayed for fold")
        copy_job_app.verify_copy_settings_selected_option(net, "finisher_fold", "vInwardTop")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_fold= "vInwardTop")
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
    +purpose: Test Fold and Stitch settings true in copy default settings page
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_copy_setting_fold_and_stitch
    +test:
        +title:test_copy_ews_copy_setting_fold_and_stitch
        +guid:d52ecacf-e516-4e13-8b7b-e1919c712417
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews_copy_setting_fold_and_stitch(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["bookletMakerOption"] = "saddleStitch"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set punch values as rightTwoPointDin")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_booklet_saddleStitch)

        time.sleep(5)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create quick set with fold and stitch option and check UI
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:300
    +asset:Copy
    +delivery_team:A3
    +feature_team:CopySendPK
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_quickset_fold_and_stitch
    +test:
        +title:test_copy_ews_quickset_fold_and_stitch
        +guid:46deac85-de57-4d82-8f84-e39012b460c8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ProductSpecSupported=Finisher & FinisherSettings=BookletMaker

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_quickset_fold_and_stitch(job, ews, spice, net, cdm, udw):  
    try:
        copy_job_app = spice.copy_ui()
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Create copy quickset")
        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi36
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

        logging.info("Verify the value displayed for booklet")
        copy_job_app.verify_copy_settings_selected_option(net, "finisher_booklet", "saddleStitch")
        copy_job_app.back_to_landing_view()

        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        logging.info("Copy Start")
        copy_job_app.start_copy()
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet= "saddleStitch")
        
        logging.info("Verify job is success")
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        qs.csc.delete_all_shortcuts()
