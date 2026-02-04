import logging
import time
import pytest
from tests.copy.ews.copy_default_settings.defaultjoboptions.defaultjoboptionsutils import *
from selenium.common.exceptions import NoSuchElementException
from tests.copy.copy_ews_combination import job_copy_applying_pages_per_sheet_two
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from dunetuf.control.device_status import DuneDeviceStatus
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.power.power import Power

copy_orientation_ele = "contentOrientation"
string_ids_content_orientation = {
    "portrait": "cPortrait",
    "landscape": "cLandscape"
    }

copy_sharpness_option_dict = {
    # """String id for element value""" 
    1: "cSharpnessOption1", # "1 - (Soft Edges)"
    2: "cNumeral2", # "2"
    3: "cOption3Normal", # "3 - (Normal)"
    4: "cNumeral4", # "4"
    5: "cSharpnessOption5" # "5 - (Sharper Edges)"
}

copy_contrast_option_dict = {
    # """String id for element value""" 
    1: "cContrastOption1", # "1 - (Less)"
    2: "cNumeral2", # "2"
    3: "cNumeral3", # "3"
    4: "cNumeral4", # "4"
    5: "cOption5Normal", # "5 - (Normal)"
    6: "cNumeral6", # "6"
    7: "cNumeral7", # "7"
    8: "cNumeral8", # "8"
    9: "cContrastOption9" # "9 - (More)"
}

def get_copy(cdm, copy_property):

    # Get scan constraints
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == copy_property:
            options=x['options']
            resultData=[]
            for optionValues in options:
                    resultData.append(optionValues['seValue'])
    return resultData
def get_scan_data(cdm):
    # Get Scan data
    cdm_copy_info = cdm.get(cdm.JOB_TICKET_COPY)
    # Extract Scan data
    scan_data = cdm_copy_info.get('src', {}).get('scan', {})
    return scan_data

def get_imageModifications_data(cdm):
    # Get imageModifications data
    cdm_copy_info = cdm.get(cdm.JOB_TICKET_COPY)
    # Extract imageModifications data
    scan_data = cdm_copy_info.get('pipelineOptions', {}).get('imageModifications', {})
    return scan_data

def get_copy_constraints(cdm, copy_property):
    # Get scan constraints
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == copy_property:
            resultData = {
                "resourceGun": x.get("resourceGun", ""),
                "propertyPointer": x.get("propertyPointer", ""),
                "min": x.get("min", {}),
                "max": x.get("max", {}),
                "step": x.get("step", {})
            }
            return resultData

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test default copy settings page
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews__default_settings_page_rendering
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews__default_settings_page_rendering
        +guid:02ffd2f9-4a09-4d90-82b5-7688b3727741
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews__default_settings_page_rendering(ews, cdm, helper):
    """Check that rendered Copy Default Job Options rendered correctly against
    the CDM.
    """
    # load Copy Default Job Options page
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)

    # Check Apply, Cancel Buttons
    assert(ews.check_exists_by_id('footer-config-job-options-button-apply') == True)
    assert(ews.check_exists_by_id('footer-config-job-options-button-cancel') == True)

    # get the def copy job data from cdm
    djo_data = DefaultJobOptionsUtils.get_default_job_options(cdm, JobType.COPY)

    # Verify the web settings value against CDM values
    if cdm.device_feature_cdm.is_color_supported():
        helper.assert_field_text('colorMode', DefaultJobOptionsUtils.color_dict[djo_data["colorMode"]])
    else:
        helper.assert_field_text('contentType', DefaultJobOptionsUtils.content_type_dict[djo_data["contentType"]])
    
    ews.driver.close()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test changing default copy settings - Apply
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-21441
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_default_settings_apply
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_default_settings_apply
        +guid:a6b4d55f-3170-47dd-a635-bd51fdab223c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale & Copy=Color

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews_default_settings_apply(ews, cdm, helper):
    """Check that rendered Copy Default Job Options are applied
    correctly.
    """
    """ TODO: Test more of the options """
    if cdm.device_feature_cdm.is_color_supported():
        def_job_options_payload = {
            'colorMode' : 'grayscale',
        }
    else:
        def_job_options_payload = {
            'contentType' : 'mixed',
        }
    
    # load Copy Default Job Options page
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)

    # get the def copy job data from cdm
    djo_data = DefaultJobOptionsUtils.get_default_job_options(cdm, JobType.COPY)

    # Prepare cdm data, actual strings to put in the settings
    def_job_options_cdm_strvalue, def_job_options_id_strvalue = \
        DefaultJobOptionsUtils.get_default_job_options_strvalue_by_id(djo_data, def_job_options_payload)

    # Select settings based on payload string vals
    DefaultJobOptionsUtils.select_default_job_options_strvalue(ews, helper, def_job_options_payload,
        def_job_options_cdm_strvalue, def_job_options_id_strvalue)

    # Test cancel
    helper.wait_for_then_click('footer-config-job-options-button-cancel')
    time.sleep(3)

    # get the def copy job data from cdm
    djo_data2 = DefaultJobOptionsUtils.get_default_job_options(cdm, JobType.COPY)

    def_job_options_cdm_strvalue2, def_job_options_id_strvalue2 = \
        DefaultJobOptionsUtils.get_default_job_options_strvalue_by_id(djo_data2, def_job_options_payload)

    for key in def_job_options_cdm_strvalue2.keys():
        assert def_job_options_cdm_strvalue2[key] == def_job_options_cdm_strvalue[key]
# Uncomment to see test failure to verify this test actually works
#        assert def_job_options_cdm_strvalue2[key] == def_job_options_id_strvalue2[key]

    # Set up settings again, cancel can reset them to CDM values
    # Select settings based on payload string vals
    DefaultJobOptionsUtils.select_default_job_options_strvalue(ews, helper, def_job_options_payload,
        def_job_options_cdm_strvalue, def_job_options_id_strvalue)

    # Apply settings
    helper.wait_for_then_click('footer-config-job-options-button-apply')
    time.sleep(3)
    # get the def copy job data from cdm
    djo_data2 = DefaultJobOptionsUtils.get_default_job_options(cdm, JobType.COPY)

    def_job_options_cdm_strvalue2, def_job_options_id_strvalue2 = \
        DefaultJobOptionsUtils.get_default_job_options_strvalue_by_id(djo_data2, def_job_options_payload)

    for key in def_job_options_cdm_strvalue2.keys():
        assert def_job_options_cdm_strvalue2[key] == def_job_options_id_strvalue2[key]

    # Reset values back to original to not affect other tests
    # Select settings based on payload string vals
    DefaultJobOptionsUtils.select_default_job_options_strvalue(ews, helper, def_job_options_payload,
        def_job_options_cdm_strvalue2, def_job_options_cdm_strvalue)

    # Apply settings
    helper.wait_for_then_click('footer-config-job-options-button-apply')
    time.sleep(3)

    djo_data2 = DefaultJobOptionsUtils.get_default_job_options(cdm, JobType.COPY)

    def_job_options_cdm_strvalue2, def_job_options_id_strvalue2 = \
        DefaultJobOptionsUtils.get_default_job_options_strvalue_by_id(djo_data2, def_job_options_payload)

    for key in def_job_options_cdm_strvalue2.keys():
        assert def_job_options_cdm_strvalue2[key] == def_job_options_cdm_strvalue[key]

    ews.driver.close()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set Pages per sheet -> 2 
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
    +name:test_copy_ews_pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_pages_per_sheet
        +guid:15cd5c8b-c7e0-4d5d-813a-be96a3967c9a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=3x5
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_pages_per_sheet(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["pipelineOptions"]["imageModifications"]["pagesPerSheet"] =  "twoUp"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set pagesPerSheet -> 2")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_applying_pages_per_sheet_two)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        #ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test to check EWS default copy settings - content orientation drop down
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-164695
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_content_orientation
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_content_orientation
        +guid:08d3b1d0-9193-11ee-931a-1370fa855400
        +dut:
            +type:Simulator
            +configuration:CopyOutputSize=Orientation
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_content_orientation(cdm, ews, net):
    # Set the locale
    locale = "en"
    
    dropDownOptions = []
    # Go to EWS-> copy-Default copy options
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    ews.helper.wait_for_loading_complete(3)

    # verifying Content Orientation dropdown title
    contentOrientDpTitle = ews.get_string_translation("cContentOrientation")
    ews.helper.assert_field_text("contentOrientation-name", contentOrientDpTitle)

    # Get CDM contentOrientation using get_scan_data function
    scan_data = get_scan_data(cdm)
    # Retrieve content orientation options from scan data, default to empty list if not found
    content_orient_options = scan_data.get("contentOrientation", [])
    # Assert if content orientation options are null or empty
    assert content_orient_options, "Content Orientation options are null or empty."

    # Get the default dropdown value based on Content Orientation options
    content_orient_string_id = string_ids_content_orientation[content_orient_options]
    default_dp_value = LocalizationHelper.get_string_translation(net, content_orient_string_id, locale)

    # Get the selected default dropdown value
    selected_pre_dropdown_value = ews.driver.find_element(By.ID, copy_orientation_ele).text
    logging.debug(F"Print selected default: {selected_pre_dropdown_value}")
    # Assert that the selected default dropdown value matches the expected default value
    ews.helper.assert_field_text(copy_orientation_ele, default_dp_value)

    # Select the default dropdown value
    ews.helper.select_from_dropdown(copy_orientation_ele, default_dp_value)
    orient_select = WebDriverWait(ews, ews.helper.default_timeout).until(lambda d: d.get_element_by_id(copy_orientation_ele))
    orient_select.click()

    # Retrieve all dropdown options
    actual_content_orient_selection_list = ews.driver.find_elements(By.XPATH, "//span[@class='mat-option-text']")
    for actual_item in actual_content_orient_selection_list:
        dropDownOptions.append(actual_item.get_attribute('textContent').strip())

    # Get CDM contentOrientation
    resultData = get_copy(cdm, "src/scan/contentOrientation")

    # verifying CDM vs EWS options length
    assert len(resultData) == len(dropDownOptions)

    # verifying CDM vs EWS  
    for index in range(0,len(dropDownOptions)):
        logging.info("Expected content orientation options: "+ ews.get_string_translation(string_ids_content_orientation[resultData[index]]))
        logging.info("Actual content orientation options: " + dropDownOptions[index])
        assert ews.get_string_translation(string_ids_content_orientation[resultData[index]]) == dropDownOptions[index]   

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test to check EWS default copy settings - Sharpness drop down
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-214961
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_sharpness_drop_down
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_sharpness_drop_down
        +guid:b585cc8e-acd0-11ef-84f0-8bac3d40f947
        +dut:
            +type:Simulator
            +configuration:DefaultCopyOptions=Contrast & DefaultCopyOptions=Sharpness
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews_sharpness_drop_down(cdm, ews, net):
    locale = "en"
    # Get CDM sharpness constraints
    resultData = get_copy_constraints(cdm, "pipelineOptions/imageModifications/sharpness")
    if resultData is not None:
        sharpnessDropDownOptions = []

        # Go to EWS-> copy-Default copy options
        ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
        ews.helper.wait_for_loading_complete(3)

        # Verifying sharpness dropdown title
        sharpnessDpTitle = ews.get_string_translation("cSharpness")
        ews.helper.assert_field_text("sharpness-name", sharpnessDpTitle)

        # Get CDM imageModifications data
        imageMod_data = get_imageModifications_data(cdm)
        # Retrieve sharpness options from imageModifications data, default to empty list if not found
        sharpness_options = imageMod_data.get("sharpness", [])
        # Assert if sharpness options are null or empty
        assert sharpness_options, "Sharpness options are null or empty."

        # Get the default dropdown value based on sharpness options
        sharpness_options_id = copy_sharpness_option_dict[sharpness_options]
        default_dp_value = LocalizationHelper.get_string_translation(net, sharpness_options_id, locale)

        # Get the selected default dropdown value
        selected_pre_dropdown_value = ews.driver.find_element(By.ID, "sharpness").text
        logging.debug(f"Print selected default: {selected_pre_dropdown_value}")
        # Assert that the selected default dropdown value matches the expected default value
        ews.helper.assert_field_text("sharpness", default_dp_value)

        # Select the default dropdown value
        ews.helper.select_from_dropdown("sharpness", default_dp_value)
        sharpness_select = WebDriverWait(ews.driver, ews.helper.default_timeout).until(lambda d: d.find_element(By.ID, "sharpness"))
        sharpness_select.click()

        # Retrieve all dropdown options
        actual_sharpness_selection_list = ews.driver.find_elements(By.XPATH, "//span[@class='mat-option-text']")
        for actual_item in actual_sharpness_selection_list:
            sharpnessDropDownOptions.append(actual_item.get_attribute('textContent').strip())

        # Verifying local values against Ews values
        assert len(copy_sharpness_option_dict) == len(sharpnessDropDownOptions)

        for index in range(0,len(sharpnessDropDownOptions)):
            expected_option = LocalizationHelper.get_string_translation(net, copy_sharpness_option_dict[index + 1], locale)
            actual_option = sharpnessDropDownOptions[index]
            logging.info(f"Expected sharpness option: {expected_option}")
            logging.info(f"Actual sharpness option: {actual_option}")
            assert expected_option == actual_option, f"Expected {expected_option}, but got {actual_option}" 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test to check EWS default copy settings - Contrast drop down
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-214961
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_contrast_drop_down
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_contrast_drop_down
        +guid:bb5cb654-acd0-11ef-8302-4fa0ddb32f6c
        +dut:
            +type:Simulator
            +configuration:DefaultCopyOptions=Contrast & DefaultCopyOptions=Sharpness
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_contrast_drop_down(cdm, ews, net):
    locale = "en"
    # Get CDM contrast constraints
    resultData = get_copy_constraints(ews.cdm, "pipelineOptions/imageModifications/contrast")
    if resultData is not None:
        contrastDropDownOptions = []

        # Go to EWS-> copy-Default copy options
        ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
        ews.helper.wait_for_loading_complete(3)

        # Verifying contrast dropdown title
        contentDpTitle = ews.get_string_translation("cContrast")
        ews.helper.assert_field_text("contrast-name", contentDpTitle)

        # Get CDM imageModifications data
        imageMod_data = get_imageModifications_data(cdm)
        # Retrieve contrast options from imageModifications data, default to empty list if not found
        contrast_options = imageMod_data.get("contrast", [])
        # Assert if contrast options are null or empty
        assert contrast_options, "Contrast options are null or empty."

        # Get the default dropdown value based on contrast options
        contrast_options_id = copy_contrast_option_dict[contrast_options]
        default_dp_value = LocalizationHelper.get_string_translation(net, contrast_options_id, locale)

        # Get the selected default dropdown value
        selected_pre_dropdown_value = ews.driver.find_element(By.ID, "contrast").text
        logging.debug(f"Print selected default: {selected_pre_dropdown_value}")
        # Assert that the selected default dropdown value matches the expected default value
        ews.helper.assert_field_text("contrast", default_dp_value)

        # Select the default dropdown value
        ews.helper.select_from_dropdown("contrast", default_dp_value)
        contrast_select = WebDriverWait(ews.driver, ews.helper.default_timeout).until(lambda d: d.find_element(By.ID, "contrast"))
        contrast_select.click()

        # Verify all dropdown options
        actual_contrast_selection_list = ews.driver.find_elements(By.XPATH, "//span[@class='mat-option-text']")
        for actual_item in actual_contrast_selection_list:
            contrastDropDownOptions.append(actual_item.get_attribute('textContent').strip())

        # Verifying CDM vs EWS options length
        assert len(copy_contrast_option_dict) == len(contrastDropDownOptions)

        # Verifying CDM vs EWS
        for index in range(0,len(contrastDropDownOptions)):
            expected_option = LocalizationHelper.get_string_translation(net, copy_contrast_option_dict[index + 1], locale)
            actual_option = contrastDropDownOptions[index]
            logging.info(f"Expected sharpness option: {expected_option}")
            logging.info(f"Actual sharpness option: {actual_option}")
            assert expected_option == actual_option, f"Expected {expected_option}, but got {actual_option}"


