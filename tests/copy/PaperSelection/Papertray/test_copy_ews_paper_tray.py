import logging
import time
import copy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from dunetuf.ews import EWS
from tests.copy.copy_ews_combination import *
from tests.copy.defaultjoboptions.defaultjoboptionsutils import DefaultJobOptionsUtils, JobType
from dunetuf.power.power import Power
from dunetuf.ssh import SSH
from dunetuf.ssh_client import SSH_CLIENT
from dunetuf.control.device_status import DuneDeviceStatus
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.emulation.print.print_emulation_ids import DuneEnginePlatform
copy_select_ids_list = []
copy_toggle_ids_list = []
copy_slider_ids_list = []
copy_email_ids_list = []
copy_text_ids_list = []

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test tray selection settings in copy settings page
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-74018
    +timeout:120
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ews_tray_selection
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_tray_selection
        +guid:56db92ec-47a6-4401-8ee5-4b0a93d355c2
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=Tray1 & JobSettings=EWSJobQueue

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator



$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_tray_selection(ews, helper, configuration):
    try:
        # load Copy Default Job Options page
        helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)

        cards = WebDriverWait(ews.driver, EWS.default_timeout).until(
            lambda d: d.find_elements(By.TAG_NAME, "mat-card-content"))
        logging.info(dir(cards[0]))

        #helper.select_from_dropdown('tray', copy_settings_def_opts.def_job_options_strings['auto'])
        helper.select_from_dropdown('paperTray', DefaultJobOptionsUtils.tray_dic['auto'])

        # check that the tray 1 is shown.
        tray_select  = WebDriverWait(ews, EWS.default_timeout).until(
            lambda d: d.get_element_by_id('paperTray'))
        tray_select.click()
        
        if configuration.familyname == "enterprise":
            expected_tray_selection_list = [DefaultJobOptionsUtils.tray_dic['auto'],
                                        DefaultJobOptionsUtils.tray_dic['manual'],
                                        DefaultJobOptionsUtils.tray_dic['tray-1'],
                                        DefaultJobOptionsUtils.tray_dic['tray-2']]
        else:
            expected_tray_selection_list = [DefaultJobOptionsUtils.tray_dic['auto'],
                                        DefaultJobOptionsUtils.tray_dic['tray-1'],
                                        DefaultJobOptionsUtils.tray_dic['tray-2']]

        # Convert expected tray selection list to a set
        expected_tray_selection_set = set(expected_tray_selection_list)

        # Get actual tray selection list and convert it to a set
        actual_tray_selection_list = ews.driver.find_elements(By.XPATH, "//span[@class='mat-option-text']")
        actual_tray_selection_set = {item.get_attribute('textContent').strip() for item in actual_tray_selection_list}
        # Check if expected tray selection set is a subset of actual tray selection set
        assert expected_tray_selection_set.issubset(actual_tray_selection_set)
        assert ews.check_exists_by_id('tray-1') is False
        assert ews.check_exists_by_id('tray-2') is False
        assert ews.check_exists_by_id('auto') is False

        time.sleep(2)
    finally:
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper tray and verify values by cdm
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
    +name:test_copy_ews_tray_manual_feed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_tray_manual_feed
        +guid:1d9a9d26-a759-40f0-8a95-15bf7aba6c5a
        +dut:
            +type:Simulator
            +configuration: DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_tray_manual_feed(ews, configuration):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSource"] = "manual" 

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set tray values as manual feed")
        job_copy_option_combi_paper_tray_manual ={
        CopyEwsOptionsKey.select_tray: PaperTray.manual_feed
        }
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_tray_manual)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
