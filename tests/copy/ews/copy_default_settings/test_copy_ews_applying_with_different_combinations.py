import logging
from tests.copy.ews.copy_default_settings.copy_ews_combination import *
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.emulation.print.print_emulation_ids import DuneEnginePlatform

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_applying_with_different_combinations_one
    +test:
        +title:test_copy_ews_applying_with_different_combinations_one
        +guid:46f67d25-5eab-4c50-b365-42db4745b149
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=GrayScale & JobSettings=EWSJobQueue
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_applying_with_different_combinations_one(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_different_combinations_one)
        ews_copy_app.click_ews_copy_page_apply_button()
        ews_copy_app.check_with_cdm_on_ews_job_copy(applying_with_different_combinations_one_expected_settings_from_actual_cdm(ews))
    finally:
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_applying_with_different_combinations_two
    +test:
        +title:test_copy_ews_applying_with_different_combinations_two
        +guid:6f058e93-bf09-4423-9cab-bc2867a356bc
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & FlatbedMediaSize=A5 & JobSettings=EWSJobQueue & MediaInputInstalled=Tray3 & CopyOutputScale=LettertoA4
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_applying_with_different_combinations_two(ews, print_emulation, reset_manager, configuration):
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

    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_different_combinations_two)
        ews_copy_app.click_ews_copy_page_apply_button()
        ews_copy_app.check_with_cdm_on_ews_job_copy(applying_with_different_combinations_two_expected_settings_from_actual_cdm(ews))
    finally:
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_applying_with_different_combinations_four
    +test:
        +title:test_copy_ews_applying_with_different_combinations_four
        +guid:bde8cb95-224a-44f5-a76a-a9c2f0019d85
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & FlatbedMediaSize=Letter & JobSettings=EWSJobQueue
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_applying_with_different_combinations_four(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_different_combinations_four)
        ews_copy_app.click_ews_copy_page_apply_button()
        ews_copy_app.check_with_cdm_on_ews_job_copy(applying_with_different_combinations_four_expected_settings_from_actual_cdm(ews))
    finally:
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set automatic color mode and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_applying_with_different_combinations_five
    +test:
        +title:test_copy_ews_applying_with_different_combinations_five
        +guid:ba4e0a03-9969-4c4a-b249-89d041e82e80
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & JobSettings=EWSJobQueue
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_applying_with_different_combinations_five(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        ews_copy_app.edit_copy_ews_setting(job_copy_applying_with_different_combinations_five)
        ews_copy_app.click_ews_copy_page_apply_button()
        ews_copy_app.check_with_cdm_on_ews_job_copy(applying_with_different_combinations_five_expected_settings_from_actual_cdm(ews))
    finally:
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)