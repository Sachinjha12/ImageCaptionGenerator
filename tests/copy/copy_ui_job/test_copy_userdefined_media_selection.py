import logging
import random
import string
import json
import re
import time
from time import sleep
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel

def load_trays(print_emulation,cdm,media):
    """
        Configures and loads the installed trays of a print emulation system with default values.

        Args:
            print_emulation (object): The print emulation object that provides access to tray operations.
            cdm (object): The Common Device Manager (CDM) object used for handling device alerts.
            media (object): The media object used to handle alert actions.

        Functionality:
            - Retrieves the list of installed trays from the print emulation system.
            - Sets the capacity of each tray to unlimited.
            - For Tray1:
                - Empties the tray.
                - Loads the tray with the 'Letter' media size.
            - For other trays:
                - Opens the tray.
                - Empties the tray.
                - Loads the tray with the 'Letter' media size.
                - Closes the tray.
            - Waits for a 'sizeType' alert and responds with 'ok' if the alert appears.
            - Logs a debug message if the 'sizeType' alert does not appear.

        Exceptions:
            - Catches and logs any exceptions that occur while waiting for the 'sizeType' alert.
    """
    # load and configure the installed trays with default values(letter and plain)
    tray_list = print_emulation.tray.get_installed_trays()
    for tray_id in tray_list:
        print_emulation.tray.capacity_unlimited(tray_id)
        if tray_id == MediaInputIds.Tray1.name:
            print_emulation.tray.empty(tray_id)
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
        else:
            print_emulation.tray.open(tray_id)
            print_emulation.tray.empty(tray_id)
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
            print_emulation.tray.close(tray_id)
        try:
            cdm.alerts.wait_for_alerts('sizeType',30)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear")

def get_random_string(length)->str:
    """
        generate a random string
    """
    result_str = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(length))
    return result_str

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Select copy job with setting paper type as User defined media type
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-151782
    +timeout:400
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_type_UserType
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_UserType
        +guid: 6a714b1d-bce1-40bb-b853-e7b821667f3f
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & ScannerInput=Flatbed & PrintEmulation=HighFidelity & ProductSpecSupported=MPModes & MediaType=UserDefined
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_UserType(spice, job, udw, net, tray,cdm,print_emulation,media):
    job.bookmark_jobs()
    try:
        expected_paper_type = get_random_string(10)
        response = cdm.get_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10")
        response_body = response.json()
        print(response_body)
        body = {
            "mediaTypeVisibleEnabled": "true", 
            "userDefinedName": expected_paper_type
        }
        r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
        if r.status_code != 204:
            counter = 0
            while counter < 5 or r.status_code != 204:
                r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
                sleep(10)
                counter = counter + 1
        assert r.status_code == 204
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.usertype-10')
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_type_option("UserType10")
        paperType_value_button=spice.wait_for(CopyAppWorkflowObjectIds.radio_paperType_user_defined_10)
        paperType_value_button.mouse_click()
        spice.copy_ui().go_to_paper_selection()
        paper_type = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperType + " SpiceText[visible=true]")["text"]
        paper_size = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSize + " SpiceText[visible=true]")["text"]
        paper_tray = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_paperTray + " SpiceText[visible=true]")["text"]
        expected_string = paper_size+", "+paper_type+", "+paper_tray
        assert paper_type == expected_paper_type
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().workflow_common_operations.is_item_available(CopyAppWorkflowObjectIds.list_copySettings_paperSelection, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, scrolling_value=0.05)
        get_paper_selection_string = spice.wait_for(CopyAppWorkflowObjectIds.view_paperSetting + " SpiceText[visible=true]")["text"]
        assert expected_string == get_paper_selection_string
        spice.copy_ui().back_to_landing_view()
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
        load_trays(print_emulation,cdm,media)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Select copy job with setting paper type as User defined media type
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-151782
    +timeout:400
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_type_UserType_Minimum
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_UserType_Minimum
        +guid: 38cff11d-cb00-4af7-a12d-02563e0792bc
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & ScannerInput=Flatbed & PrintEmulation=HighFidelity & MediaType=UserDefined
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_UserType_Minimum(spice, job, udw, net, tray,cdm,print_emulation,media):
    job.bookmark_jobs()
    try:
        expected_paper_type = "a"
        response = cdm.get_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10")
        response_body = response.json()
        print(response_body)
        body = {
            "mediaTypeVisibleEnabled": "true", 
            "userDefinedName": expected_paper_type
        }
        r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
        if r.status_code != 204:
            counter = 0
            while counter < 5 or r.status_code != 204:
                r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
                sleep(10)
                counter = counter + 1
        assert r.status_code == 204
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.usertype-10')
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_type_option("UserType10")
        paperType_value_button=spice.wait_for(CopyAppWorkflowObjectIds.radio_paperType_user_defined_10)
        paperType_value_button.mouse_click()
        # spice.copy_ui().go_to_paper_selection()
        paper_type = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperType + " SpiceText[visible=true]")["text"]
        paper_size = spice.wait_for(CopyAppWorkflowObjectIds.view_copySettings_paperSize + " SpiceText[visible=true]")["text"]
        paper_tray = spice.wait_for(CopyAppWorkflowObjectIds.combo_copySettings_paperTray + " SpiceText[visible=true]")["text"]
        expected_string = paper_size+", "+paper_type+", "+paper_tray
        assert paper_type == expected_paper_type
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().workflow_common_operations.is_item_available(CopyAppWorkflowObjectIds.list_copySettings_paperSelection, CopyAppWorkflowObjectIds.view_copySettingsView, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar, scrolling_value=0.05)
        get_paper_selection_string = spice.wait_for(CopyAppWorkflowObjectIds.view_paperSetting + " SpiceText[visible=true]")["text"]
        assert expected_string == get_paper_selection_string
        spice.copy_ui().back_to_landing_view()
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
        load_trays(print_emulation,cdm,media)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the disabled user-defined media type is not listed in the copy paper selection.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-151782
    +timeout:400
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_type_UserType_Disabled
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_UserType_Disabled
        +guid: cd832f87-2ff9-43bc-8ce9-db3c7160ab80
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & ScannerInput=Flatbed & PrintEmulation=HighFidelity & MediaType=UserDefined
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_UserType_Disabled(spice, job, udw, net, tray,cdm,print_emulation,media):
    job.bookmark_jobs()
    try:
        expected_paper_type = get_random_string(10)
        response = cdm.get_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10")
        response_body = response.json()
        print(response_body)
        body = {
            "mediaTypeVisibleEnabled": "false",
            "userDefinedName": expected_paper_type
        }
        r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
        if r.status_code != 204:
            counter = 0
            while counter < 5 or r.status_code != 204:
                r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
                sleep(10)
                counter = counter + 1
        assert r.status_code == 204
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, default_paper_size, 'com.hp.usertype-10')
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_type_option("UserType10")
        assert spice.check_item(CopyAppWorkflowObjectIds.radio_paperType_user_defined_10) == None
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
        load_trays(print_emulation,cdm,media)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the Paper Type Mismatch error for user-defined media type wih copy job.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-151782
    +timeout:400
    +asset: Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_flatbed_landingpage_paper_type_UserType_PaperTypeMismatch
    +test:
        +title: test_copy_ui_flatbed_landingpage_paper_type_UserType_PaperTypeMismatch
        +guid: e71161ed-2dee-40f3-838f-9265bc4d61be
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & Copy=PaperType & ScannerInput=Flatbed & PrintEmulation=HighFidelity & MediaType=UserDefined
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_paper_type_UserType_PaperTypeMismatch(spice, job, udw, net, tray, cdm, print_emulation, configuration, media, locale: str = "en"):
    job.bookmark_jobs()
    try:
        expected_paper_type = "UserType10"
        excepttedalert = "Load Paper in Tray 2"
        response = cdm.get_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10")
        response_body = response.json()
        print(response_body)
        body = {
            "mediaTypeVisibleEnabled": "true",
            "userDefinedName": expected_paper_type
        }
        r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
        if r.status_code != 204:
            counter = 0
            while counter < 5 or r.status_code != 204:
                r = cdm.patch_raw(cdm.PRINTMODES_MEDIA_CONFIGURATION_ENDPOINT_V2 + "/com.hp.usertype-10", body)
                sleep(10)
                counter = counter + 1
        assert r.status_code == 204
        default = tray.get_default_source()
        default_paper_size = tray.get_default_size(default)
        tray.configure_tray(default, 'iso_a1_594x841mm', 'stationery')
        print_emulation.tray.open(MediaInputIds.Tray2.name)
        tray.configure_tray('tray-2', 'iso_a4_210x297mm', 'stationery')
        print_emulation.tray.close(MediaInputIds.Tray2.name)
        try:
            cdm.alerts.wait_for_alerts('sizeType',30)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear")
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().select_paper_type_option("UserType10")
        paperType_value_button=spice.wait_for(CopyAppWorkflowObjectIds.radio_paperType_user_defined_10)
        paperType_value_button.mouse_click()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded = False)
        job_ids = job.get_recent_job_ids()
        alert = spice.wait_for(MenuAppWorkflowObjectIds.alertApp_click_alertHeader,60)
        assert alert["text"] == excepttedalert, "Alert message is not as expected"
        current_string = spice.query_item(CopyAppWorkflowObjectIds.load_paper_alert_detail, 2)["text"]
        assert expected_paper_type in current_string, "Paper type mismatch in alert"
        logging.info("current_string: " + current_string)
        ok_btn = spice.wait_for(CopyAppWorkflowObjectIds.copy_load_paper_hide, 60)
        ok_btn.mouse_click()
        logging.info("hide: clicked ")
        logging.info("Cancel all active jobs")
        job.cancel_active_jobs()
        logging.info("Wait for no active jobs")
        job.wait_for_no_active_jobs()
        # Validate paper type in tray empty alert
        if tray.is_size_supported('iso_a4_210x297mm', 'tray-2'):
            tray.configure_tray('tray-2', 'iso_a1_594x841mm', 'com.hp.usertype-10')
        print_emulation.tray.open("Tray2")
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.empty(tray2)
        print_emulation.tray.close(tray2)
        cdm.alerts.wait_for_alerts("outOfMedia")
        alert_body = spice.query_item(CopyAppWorkflowObjectIds.load_paper_alert_detail,0)
        alert_body_string = str(alert_body["text"])
        assert expected_paper_type in alert_body_string ,"Paper type mismatch in alert"
        print_emulation.tray.close("Tray2")
        assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp,60)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()
        load_trays(print_emulation,cdm,media)
