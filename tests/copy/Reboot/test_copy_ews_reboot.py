import logging
import time
from tests.copy.ews.copy_default_settings.defaultjoboptions.defaultjoboptionsutils import *
from tests.copy.copy_ews_combination import *
from dunetuf.ews.CopyEws import *
from dunetuf.power.power import Power
from dunetuf.control.device_status import DuneDeviceStatus



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set Pages per sheet -> 2
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:900
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_reboot_check_default_setting
    +test:
        +title:test_copy_ews_reboot_check_default_setting
        +guid:25d6a57d-c93c-4e63-874a-505df99fcec2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_reboot_check_default_setting(ews,udw,net,cdm):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        job_copy_option_default = {
            CopyEwsOptionsKey.number_of_copies: 10,
            }
        ews_copy_app.load_jobs_copy_page()
        logging.info("set no of copies to 10")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_default)
        ews_copy_app.click_ews_copy_page_apply_button()
        Power(udw).power_cycle()
        # ssh.run("reboot")
        time.sleep(60)
        # wait for system to reboot
        device_status = DuneDeviceStatus(net.ip_address,"")
        result = device_status.device_ready(300)
        assert all(result.values())
        ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
        assert ticket_default_response.status_code == 200
        ticket_default_body = ticket_default_response.json()
        default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"]
        assert default_dest_print_copies == 10

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set Pages per sheet -> 2 on engine
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_reboot_check_default_setting_engine
    +test:
        +title:test_copy_ews_reboot_check_default_setting_engine
        +guid:b4464933-c5c3-4f9f-afad-733b7c4d911a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_reboot_check_default_setting_engine(ews,udw,net,cdm,reset_manager):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        job_copy_option_default = {
            CopyEwsOptionsKey.number_of_copies: 10,
            }
        ews_copy_app.load_jobs_copy_page()
        logging.info("set no of copies to 10")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_default)
        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("Reboot the device and wait device ready")
        reset_manager.reboot_printer()
        reset_manager.wait_for_device_ready()
        ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
        assert ticket_default_response.status_code == 200
        ticket_default_body = ticket_default_response.json()
        default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"]
        assert default_dest_print_copies == 10

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
