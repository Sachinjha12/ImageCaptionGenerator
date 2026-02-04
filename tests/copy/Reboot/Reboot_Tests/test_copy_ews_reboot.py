import pytest
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from dunetuf.ews import EWS
from tests.copy.defaultjoboptions.defaultjoboptionsutils import DefaultJobOptionsUtils, JobType
from dunetuf.power.power import Power
from dunetuf.ssh import SSH
from dunetuf.ssh_client import SSH_CLIENT
from dunetuf.control.device_status import DuneDeviceStatus

copy_select_ids_list = []
copy_toggle_ids_list = []
copy_slider_ids_list = []
copy_email_ids_list = []
copy_text_ids_list = []

@pytest.fixture(autouse=True)
def setup_teardown_copy_ews_reboot(device_manager):
    """Setup/teardown"""
    mechless = device_manager.get_boot_mode()

    yield

    # Make sure mechless is set back to the pre-test value
    device_manager.set_boot_mode(mechless)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test tray selection settings option in copy settings screen after a power reset.
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-74018
    +timeout:480
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ews_tray_selection_power_reset
    +test:
        +title: test_copy_ews_tray_selection_power_reset
        +guid:f1125c1f-7006-43c5-8ef2-a6dd1e143d17
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
def test_copy_ews_tray_selection_power_reset(ews, ssh, net, helper, udw):

    try:
        # load Copy Default Job Options page
        helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)

        cards = WebDriverWait(ews.driver, EWS.default_timeout).until(
            lambda d: d.find_elements(By.TAG_NAME, "mat-card-content"))
        helper.select_from_dropdown(
            'paperTray', DefaultJobOptionsUtils.tray_dic['tray-1'])

        # reboot sequence
        helper.ews.close_browser()
        Power(udw).power_cycle()
        # ssh.run("reboot")
        time.sleep(60)

        # wait for system to reboot
        device_status = DuneDeviceStatus(net.ip_address,"")
        result = device_status.device_ready(300)
        assert all(result.values())

        # load USB Default Job Options page
        ews.load("/copy/defaultJobOptions")

        cards = WebDriverWait(ews.driver, EWS.default_timeout).until(
            lambda d: d.find_elements(By.TAG_NAME, "mat-card-content"))
        logging.info(dir(cards[0]))

        actual_tray_selection_list = ews.driver.find_elements(By.XPATH,
                "//span[@class='mat-option-text']")

        helper.assert_field_text(
            'paperTray', DefaultJobOptionsUtils.tray_dic['auto'])

    finally:
        logging.info("end of test")

def apply_restore_factory_default(ews):
    ews.networkEWS.load_restore_network_defaults_page()
    ews.helper.wait_for_then_click('restoreAllFactoryDefaultCardExpand')
    ews.helper.wait_for_then_click('restore-factory')
    ews.helper.wait_for_then_click("restore-confirmation")
    ews.helper.wait_for_loading_complete(180)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Tray selection settings option to defaults after a factory restore
    +test_tier: 1
    +is_manual: False
    +reqid: DUNE-74018
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ews_tray_selection_factory_restore
    +test:
        +title: test_copy_ews_tray_selection_factory_restore
        +guid:e03d7c83-4331-45c2-8897-63854b05d2e2
        +dut:
            +type: Emulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset & ScannerInput=Flatbed


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_tray_selection_factory_restore(ews, ssh, net, helper, udw, reset_manager):

    # once printer boots up, verify the Type variable persists. This confirms that you've successfully paired your printer as an HP Traditional device.
    persona = udw.mainApp.PersonaManager.getPersona()
    logging.info(persona)
    if persona != "TRADITIONAL":
        raise Exception("Factory restory should be done in Flex mode, but you're in {0}".format(persona))

    try:
        # load Copy Default Job Options page
        helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)

        cards = WebDriverWait(ews.driver, EWS.default_timeout).until(
            lambda d: d.find_elements(By.TAG_NAME, "mat-card-content"))
        logging.info(dir(cards[0]))

        helper.select_from_dropdown(
            'paperTray', DefaultJobOptionsUtils.tray_dic['tray-1'])

        # factory restore sequence
        apply_restore_factory_default(ews)
        
        # Wait for device to be fully ready after factory reset
        reset_manager.wait_for_device_ready(timeout=600)

        # load USB Default Job Options page
        ews.load("/copy/defaultJobOptions")

        cards = WebDriverWait(ews.driver, EWS.default_timeout).until(
            lambda d: d.find_elements(By.TAG_NAME, "mat-card-content"))
        logging.info(dir(cards[0]))

        helper.assert_field_text(
            'paperTray', DefaultJobOptionsUtils.tray_dic['auto'])

    finally:
        logging.info("end of test")
