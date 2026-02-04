import logging
import copy
import pytest
from dunetuf.copy.copy import *
from tests.send.quicksets.email.email_combination import *
from tests.send.quicksets.scantousb.usb_combination import *
from tests.send.quicksets.folder.network_folder_combination import *
from tests.send.quicksets.quicksets_common import *
from tests.copy.quicksets.copy_common import verify_create_copy_quick_set_from_ews, verify_create_copy_quick_set_from_ews_standard_doc_add_pages,\
                                             check_with_cdm_on_ews_quick_sets_copy,\
                                             check_quickset_order_by_quick_set_name, check_quickset_order_by_quick_set_type,\
                                             check_quickset_order_by_start_option, expected_cdm_for_copy_default_from_actual_cdm
from tests.copy.quicksets.copy_combination import *
from tests.send.quicksets.quicksets_common import get_local_time
from dunetuf.ews.JobsOptionsSupportedEws import ScanPayloadValues

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with default settings and press start from landing
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_defaultsettings_startoption_from_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_defaultsettings_startoption_from_landingapp
        +guid:8843018f-5fa9-4e9b-8506-0456cc02ecab
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
@pytest.mark.disable_autouse
def test_copy_quickset_ews_add_defaultsettings_startoption_from_landingapp(ews):
    try:
        update_excepted_results = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_excepted_results["summary_info"]["action"] = "open"
        if ews.cdm.device_feature_cdm.is_color_supported()== False:
            update_excepted_results["settings_info"]["src"]["scan"]["colorMode"] = "grayscale"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_excepted_results,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with combi3 settings and start automatically when select
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_home
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_home
        +guid:126f7697-bbe9-4c90-80b7-b58775dacf2d
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Letter & EWS=Quicksets
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_quickset_ews_add_customsettings_start_from_home(ews):
    try:
        expected_cdm = expected_cdm_copy_combi3_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=copy_option_combi3
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with combi2 settings and press start from landing
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_add_customsettings_start_from_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_add_customsettings_start_from_landingapp
        +guid:16a1ac95-7dcf-4c37-b269-cb5b991e1a20
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy  & FlatbedMediaSize=Custom
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_quickset_ews_add_customsettings_start_from_landingapp(ews):
    # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
    try:
        expected_cdm = expected_cdm_copy_combi2_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi2
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Delete copy quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_delete
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_delete
        +guid:b71b3ef5-78f0-4f63-8c89-8b307e4c546c
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
@pytest.mark.disable_autouse
def test_copy_quickset_ews_delete(spice, ews):
    try:
        updated_expected_settings_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        # Create copy quickset with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=updated_expected_settings_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser and delete the quickset
        qs = ews.quick_sets_app
        qs.delete_quick_set_by_title(copy_title_name)

        qs.csc.get_shortcut_id(copy_title_name) == 0, f"failed to delete"

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(copy_title_name)
        assert qs_index == -1, "Failed to delete corresponding quickset"
        # no need to cleanup since this test checking point is deleting Quickset

        menu_app = spice.homeMenuUI()
        logging.info("Perform quickset job from FP of menu app")
        menu_app.goto_menu_quickSets(spice)
        spice.copy_ui().check_copy_delete_quickset_successfully(copy_title_name)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        spice.goto_homescreen()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Edit copy quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_edit
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_edit
        +guid:14789d5e-1537-4801-adbf-8689d41833e2
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & FlatbedMediaSize=Letter & EWS=Quicksets

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_quickset_ews_edit(ews, udw):
    udw.mainApp.ScanMedia.loadMedia("ADF")
    try:
        expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        updated_copy_title_name = f"{copy_title_name}_{get_local_time()}"
        # Create copy quick set with default settings
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser to edit the quickset
        qs = ews.quick_sets_app
        qs.start_to_edit_quick_set_by_title(copy_title_name)
        # Modify form content
        qs.complete_copy_quick_sets_from_setup_page(
            title=updated_copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi3
        )

        logging.info("Check quickset in EWS")
        qs_index = qs.find_quick_set_by_title(updated_copy_title_name)
        assert qs_index != -1
        # Check in cdm
        updated_expected_settings_cdm = expected_cdm_copy_combi3_from_actual_cdm(ews)
        updated_expected_settings_cdm ["summary_info"]["title"] = updated_copy_title_name
        updated_expected_settings_cdm ["summary_info"]["action"] = "open"
        check_with_cdm_on_ews_quick_sets_copy(qs, updated_copy_title_name, updated_expected_settings_cdm)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(updated_copy_title_name)

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Filter copy quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:900
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_filter
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_filter
        +guid:307b31f2-fba5-4666-9649-ee3f0678055a
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=DigitalSend & Connectivity=USBHost & ScanDestination=Email & ScanDestination=NetworkFolder & ScannerInput=Flatbed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_quickset_ews_filter(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        if ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value) and ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value):
            email_addresses_settings_default.update({
                EmailAddressesSettingsKey.cc: EmailCc.specify_address,
                EmailAddressesSettingsKey.cc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
                EmailAddressesSettingsKey.bcc: EmailBcc.specify_address,
                EmailAddressesSettingsKey.bcc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
            })

        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[0],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[1],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[2],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[3],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        qs.create_copy_quick_sets(
            title=copy_quicksets_name_list[4],
            description=copy_description,
            start_option=QuickSetStartOption.start_automatically,
            copy_options=None
        )

        qs.create_scan_email_quick_sets(
            title=copy_quicksets_name_list[5],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.start_automatically,
            email_options=None
        )

        qs.create_scan_email_quick_sets(
            title=copy_quicksets_name_list[6],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.start_automatically,
            email_options=None
        )

        qs.create_scan_usb_quick_sets(
            title=copy_quicksets_name_list[7],
            description=usb_description,
            start_option=QuickSetStartOption.start_automatically,
            usb_options=None
        )

        qs.create_scan_usb_quick_sets(
            title=copy_quicksets_name_list[8],
            description=usb_description,
            start_option=QuickSetStartOption.start_automatically,
            usb_options=None
        )

        qs.create_scan_net_folder_quick_sets(
            title=copy_quicksets_name_list[9],
            net_folder_settings=net_folder_settings_default,
            description=network_folder_description,
            start_option=QuickSetStartOption.start_automatically,
            folder_options=None
        )

        check_filter_by_quick_set_type(
            qs_app=qs,
            title_list=[
                'Auto_Test_Quick_Set_Copy1',
                'Auto_Test_Quick_Set_Copy2',
                'Auto_Test_Quick_Set_Copy3',
                'Auto_Test_Quick_Set_Copy4',
                'Auto_Test_Quick_Set_Copy5',
            ],
            filter_name=FilterQuicksetTypeShowName.copy,
            filter_type= FilterQuicksetType.copy,
        )

        check_filter_by_quick_set_type_cdm(
            qs_app=qs,
            title_list=[
                'Auto_Test_Quick_Set_Copy1',
                'Auto_Test_Quick_Set_Copy2',
                'Auto_Test_Quick_Set_Copy3',
                'Auto_Test_Quick_Set_Copy4',
                'Auto_Test_Quick_Set_Copy5',
            ],
            filter_type= FilterQuicksetTypeCDM.copy

        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        for i in copy_quicksets_name_list:
            qs.csc.shortcuts_init(i)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Sort quickset by quick set name
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_filter_by_quicksetname
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_filter_by_quicksetname
        +guid:68adea95-f9a3-4526-a67b-fb4062f1b2d7
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed  & EWS=Quicksets

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator



$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_filter_by_quicksetname(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        if ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value) and ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value):
            email_addresses_settings_default.update({
                EmailAddressesSettingsKey.cc: EmailCc.specify_address,
                EmailAddressesSettingsKey.cc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
                EmailAddressesSettingsKey.bcc: EmailBcc.specify_address,
                EmailAddressesSettingsKey.bcc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
            })

        for i in quicksets_name_list[0:5]:
            qs.create_copy_quick_sets(
                title=i,
                description=copy_description,
                start_option=QuickSetStartOption.start_automatically,
                copy_options=None
            )

        for x in quicksets_name_list[5:7]:
            qs.create_scan_email_quick_sets(
                title=x,
                email_address_settings=email_addresses_settings_default,
                description=email_description,
                start_option=QuickSetStartOption.user_presses_start,
                email_options=None
            )

        for y in quicksets_name_list[7:9]:
            qs.create_scan_usb_quick_sets(
                title=y,
                description=usb_description,
                start_option=QuickSetStartOption. user_presses_start,
                usb_options=None
            )

        qs.create_scan_net_folder_quick_sets(
            title=quicksets_name_list[9],
            net_folder_settings=net_folder_settings_default,
            description=network_folder_description,
            start_option=QuickSetStartOption.user_presses_start,
            folder_options=None
        )
        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser
        qs = ews.quick_sets_app
        check_quickset_order_by_quick_set_name(qs)
    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Sort quickset by quick set type
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_filter_by_quicksettype
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_filter_by_quicksettype
        +guid:8e4ab78a-9934-4eba-a212-77211fc02794
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_filter_by_quicksettype(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        if ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value) and ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value):
            email_addresses_settings_default.update({
                EmailAddressesSettingsKey.cc: EmailCc.specify_address,
                EmailAddressesSettingsKey.cc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
                EmailAddressesSettingsKey.bcc: EmailBcc.specify_address,
                EmailAddressesSettingsKey.bcc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
            })

        for i in quicksets_name_list[0:5]:
            qs.create_copy_quick_sets(
                title=i,
                description=copy_description,
                start_option=QuickSetStartOption.start_automatically,
                copy_options=None
            )
        
        qs.create_scan_email_quick_sets(
            title=quicksets_name_list[5],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.user_presses_start,
            email_options=None
        )

        qs.create_scan_email_quick_sets(
            title=quicksets_name_list[6],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.user_presses_start,
            email_options=None
        )

        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser
        qs = ews.quick_sets_app
        check_quickset_order_by_quick_set_type(qs)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Sort quickset by start immediately
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_filter_by_start_immediately
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_filter_by_start_immediately
        +guid:246e65d2-cc14-4017-b8e3-3e79c114b10e
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_filter_by_start_immediately(ews, spice):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        if ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value) and ews.jobs_options_supported_ews.IsPayloadSupported(ScanPayloadValues.CC_SUPPORTED.value):
            email_addresses_settings_default.update({
                EmailAddressesSettingsKey.cc: EmailCc.specify_address,
                EmailAddressesSettingsKey.cc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
                EmailAddressesSettingsKey.bcc: EmailBcc.specify_address,
                EmailAddressesSettingsKey.bcc_address: "dsuser02@ds2016.boi.rd.hpicorp.net",
            })

        for i in quicksets_name_list[0:8]:
            qs.create_copy_quick_sets(
                title=i,
                description=copy_description,
                start_option=QuickSetStartOption.start_automatically,
                copy_options=None
            )

        qs.create_scan_email_quick_sets(
            title=quicksets_name_list[8],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.user_presses_start,
            email_options=None
        )

        qs.create_scan_email_quick_sets(
            title=quicksets_name_list[9],
            email_address_settings=email_addresses_settings_default,
            description=email_description,
            start_option=QuickSetStartOption.user_presses_start,
            email_options=None
        )
    
        logging.info("Close the current browser")
        ews.close_browser()
        # Reopen browser
        qs = ews.quick_sets_app
        check_quickset_order_by_start_option(qs)

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.delete_all_shortcuts()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with max length quicksetname
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetname_max_length
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetname_max_length
        +guid:d8402776-f6e5-4eef-b2bc-50e0aa8705da
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""   
def test_copy_quickset_ews_quicksetname_max_length(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["title"] = valid_255_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=valid_255_characters,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(valid_255_characters)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with special quicksetname
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetname_special_characters
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetname_special_characters
        +guid:f8863b9a-9d5e-46db-9d12-e979d8e3204e
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_quicksetname_special_characters(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["title"] = valid_special_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=valid_special_characters,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(valid_special_characters)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with min length quicksetname
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetname_min_length
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetname_min_length
        +guid:cc883488-f724-44c6-9819-dde269b5af90
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & ScannerInput=Flatbed & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_quicksetname_min_length(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["title"] = valid_one_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=valid_one_characters,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(valid_one_characters)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with max length quicksetdescription
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetdescription_max_length
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetdescription_max_length
        +guid:51926c75-e9a2-4bc2-b75d-204caad9b25b
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_quickset_ews_quicksetdescription_max_length(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = valid_255_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=copy_title_name,
            description=valid_255_characters,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with special quicksetdescription
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetdescription_special_characters
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetdescription_special_characters
        +guid:719924f2-1023-407f-85fa-70ef8ed3d257
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_quickset_ews_quicksetdescription_special_characters(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = valid_special_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=copy_title_name,
            description=valid_special_characters,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with min length quicksetdescription
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_quicksetdescription_min_length
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_quickset_ews_quicksetdescription_min_length
        +guid:d868905c-eeb6-470c-b801-10aceb9b4855
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_quickset_ews_quicksetdescription_min_length(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = valid_one_characters
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=copy_title_name,
            description=valid_one_characters,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with no quicksetdescription
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_no_quicksetdescription
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_no_quicksetdescription
        +guid:7367aaa9-f833-4db7-b4cf-cfa4e283a5e2
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_quickset_ews_no_quicksetdescription(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["description"] = ""
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=copy_title_name,
            description=None,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Delete all quicksets to check string and created copy quickset successful 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_no_quicksetpresent
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_no_quicksetpresent
        +guid:acc69e62-4d55-4212-bd91-04ce581c6cf0
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_no_quicksetpresent(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets")
        qs.csc.delete_all_shortcuts()

        logging.info("Check empty quickset table text")
        qs.load_self()
        qs.check_empty_quickset_table_prompt_text("This table is empty.")
        logging.info("Succeed to delete all existing quicksets")
        update_expected_cdm = expected_cdm_for_copy_default_from_actual_cdm(ews)
        update_expected_cdm["summary_info"]["action"] = "open"
        verify_create_copy_quick_set_from_ews(
            ews=ews,
            expected_settings_cdm=update_expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=None
        )

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Click cancel button when adding quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_cancel_operation_while_adding_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_cancel_operation_while_adding_quickset
        +guid:937cd681-bc29-41a7-bdba-a518023f433e
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_quickset_ews_cancel_operation_while_adding_quickset(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()

        logging.info("Select Copy and click cancel button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_cancel_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Click add buttons")
        qs.click_add_button_to_add_quick_sets()
        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()

        logging.info("Enter quickset name and click cancel button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_cancel_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that confirmation pop up window is shown with cancel and exit button")
        qs.check_if_confirm_dialog_open_with_cancel_exit_buttons()

        logging.info("Click cancel button")
        qs.click_cancel_btn_on_cancel_quickset_dialog()
        logging.info("Verify that ews show name screen")
        qs.check_name_setup_screen_active_status("true")

        logging.info("Again click cancel button at name screen")
        qs.click_cancel_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that confirmation pop up window is shown with cancel and exit button")
        qs.check_if_confirm_dialog_open_with_cancel_exit_buttons()

        logging.info("Click close button")
        qs.click_close_btn_on_cancel_quickset_dialog()
        logging.info("Verify that pop up window is closed")
        qs.check_confirm_dialog_exists(False)
        logging.info("Verify that ews show name screen")
        qs.check_name_setup_screen_active_status("true")

        logging.info("Again click cancel button at name screen")
        qs.click_cancel_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that confirmation pop up window is shown with cancel and exit button")
        qs.check_if_confirm_dialog_open_with_cancel_exit_buttons()

        logging.info("Click on exit button")
        qs.click_exit_btn_on_cancel_quickset_dialog()
        logging.info("Verify that quickset setup is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        assert short_cut_id == 0

    finally:
        logging.info("Close the current browser")
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Click close button when adding quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_close_button_operation_while_adding_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_close_button_operation_while_adding_quickset
        +guid:e1f4e393-64b5-42bd-95f1-16c4596ec955
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_close_button_operation_while_adding_quickset(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()
        logging.info("Verify that quicksets setup dialog pops up")
        qs.check_quick_sets_setup_dialog_exists(True)

        logging.info("Click on close button to close window")
        qs.click_close_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        filter_quick_sets = qs.csc.filter_quick_set_by_type_cdm(FilterQuicksetTypeCDM.copy)
        assert len(filter_quick_sets["shortcuts"]) == 0

    finally:
        logging.info("Close the current browser")
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Click finish button when adding quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_finish_operation_while_adding_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_finish_operation_while_adding_quickset
        +guid:7e3d615c-01e7-44dd-b7d4-f1ba97ba042c
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_finish_operation_while_adding_quickset(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()

        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()

        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()

        logging.info("Click finish button")
        qs.click_finish_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate to finish screen")
        qs.check_finish_setup_screen_active_status("true")
        logging.info("Checked cancel and back button grayed out")
        qs.check_cancel_button_disabled_status("true")
        qs.check_back_button_disabled_status("true")
        
        logging.info("Click on ok button")
        qs.click_ok_btn_on_quick_set_page()
        logging.info("Verify that quicksets setup dialog is closed")
        qs.check_quick_sets_setup_dialog_exists(False)

        logging.info("Check in cdm")
        filter_quick_sets = qs.csc.filter_quick_set_by_type_cdm(FilterQuicksetTypeCDM.copy)
        assert copy_title_name == (filter_quick_sets["shortcuts"][0])["title"]

    finally:
        logging.info("Close the current browser")
        ews.close_browser()
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Click back button when adding quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_back_button_operation_while_adding_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_back_button_operation_while_adding_quickset
        +guid:d0ff5905-7af8-4b7b-b91f-f6c299b605f5
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & DeviceFunction=Quickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_back_button_operation_while_adding_quickset(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Select Quicksets and click add button in ews")
        qs.load_self()
        qs.click_add_button_to_add_quick_sets()

        logging.info("Select Copy and click next button")
        qs.select_quick_sets_type(QuicksetType.copy)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Verify that ews navigate to name screen")
        qs.check_name_setup_screen_active_status("true")

        logging.info("Enter quickset name and click next button")
        qs.input_quick_sets_title(copy_title_name)
        qs.click_next_btn_on_quick_set_page()
        logging.info("Verify that ews navigate to options screen")
        qs.check_options_setup_screen_active_status("true")

        logging.info("Click back button")
        qs.click_back_btn_on_quick_sets_setup_dialog()
        logging.info("Verify that ews navigate back to name screen")
        qs.check_name_setup_screen_active_status("true")
        qs.check_options_setup_screen_active_status("false")

        logging.info("Check in cdm")
        short_cut_id = qs.csc.get_shortcut_id(copy_title_name)
        assert short_cut_id == 0

    finally:
        logging.info("Close the current browser")
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Filter copy quickset to check empty result
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28198
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_filter_no_items_found
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_filter_no_items_found
        +guid:aa7fa492-5a67-47d6-a448-0436a819c334
        +dut:
            +type:Simulator
            +configuration: DeviceFunction=Copy & Quicksets=DefaultQuickset

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_quickset_ews_filter_no_items_found(ews):
    try:
        qs = ews.quick_sets_app
        logging.info("Delete all quicksets firstly")
        qs.csc.delete_all_shortcuts()

        logging.info("Open ews and select copy in filter dropdown")
        qs.load_self()
        qs.filter_quick_set_by_type(FilterQuicksetType.copy)
        
        logging.info("Check no quick sets found in ews")
        qs.check_empty_quickset_table_prompt_text("No items were found.")
        logging.info("Check yellow exclamation mark shown in ews")
        qs.check_yellow_exclamation_mark_exists(True)

        logging.info("Check empty filter result in cdm")
        filter_quick_sets = qs.csc.filter_quick_set_by_type_cdm(FilterQuicksetTypeCDM.copy)
        assert len(filter_quick_sets["shortcuts"]) == 0, "Failed to check empty filter result in cdm"

    finally:
        logging.info("Close the current browser")
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create copy quickset with std document, add pages settings and verify with cdm values
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-24412
    +timeout:256
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_quickset_ews_scan_mode_standard_doc_add_pages
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_quickset_ews_scan_mode_standard_doc_add_pages
        +guid:223d6a42-436f-11ef-8907-336e804d512c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_quickset_ews_scan_mode_standard_doc_add_pages(ews):
    # this test will be failed since custom size is not showed in EWS and we submit issue https://hp-jira.external.hp.com/browse/HMDE-564 and it still under confirmation
    try:
        expected_cdm = expected_cdm_copy_combi_standard_doc_add_pages_from_actual_cdm(ews)
        verify_create_copy_quick_set_from_ews_standard_doc_add_pages(
            ews=ews,
            expected_settings_cdm=expected_cdm,
            title=copy_title_name,
            description=copy_description,
            start_option=QuickSetStartOption.user_presses_start,
            copy_options=copy_option_combi_standard_doc_add_pages
        )

    finally:
        logging.info("Clean up quickset when finish test")
        qs = ews.quick_sets_app
        qs.csc.shortcuts_init(copy_title_name)
