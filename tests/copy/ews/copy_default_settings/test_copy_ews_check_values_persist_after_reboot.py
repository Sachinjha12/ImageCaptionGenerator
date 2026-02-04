import logging
import time
from dunetuf.power.power import Power
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.emulation.print.print_emulation_ids import DuneEnginePlatform
from tests.copy.ews.copy_default_settings.copy_ews_combination import *

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:verify the values after printer reboot
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:800
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_check_values_persist_after_reboot
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_check_values_persist_after_reboot
        +guid:48c1f088-97ba-4b44-9345-a0f8be15c723
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & FlatbedMediaSize=A4 & MediaInputInstalled=Tray3 & JobSettings=EWSJobQueue

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:800
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_check_values_persist_after_reboot(udw,configuration,reset_manager,print_emulation,ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        if configuration.familyname == "enterprise":
            if print_emulation.print_engine_platform == DuneEnginePlatform.emulator.name: 
                tray_list=print_emulation.tray.get_installed_trays()
                logging.info('The available trays are %s', tray_list)
                tray3= MediaInputIds.Tray3.name
                if tray3 not in tray_list:
                    print_emulation.tray.install(tray3)
                    # Rebooting device after install tray3
                    print_emulation.power.restart_formatter()
                    reset_manager.wait_for_device_ready()
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set the options for copy")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_reboot)
        logging.info("get the values for element")
        element_value = ews_copy_app.get_current_values_of_options_from_page(custom_existence= 50)

        ews_copy_app.click_ews_copy_page_apply_button()
        logging.info("get the values for element")
        update_element_value = ews_copy_app.get_current_values_of_options_from_page(custom_existence= 50)
        logging.info("compare the data before and after")
        assert element_value == update_element_value, "The data is different"
        ews.close_browser()
        logging.info("reboot the printer")
        # powercycle the printer
        Power(udw).power_cycle()
        ews.is_systemStatusReady()
        time.sleep(5)

        logging.info("load the job copy page again")
        ews_copy_app.load_jobs_copy_page()
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(excepted_reboot_settings_from_actual_cdm(ews))

        logging.info("get the values for element")
        new_update_element_value = ews_copy_app.get_current_values_of_options_from_page(custom_existence= 50)

        logging.info("compare the data before and after")
        assert update_element_value == new_update_element_value, "The data is different"

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()
