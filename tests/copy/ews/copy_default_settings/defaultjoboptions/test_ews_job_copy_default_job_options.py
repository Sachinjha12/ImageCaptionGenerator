import pytest
import logging
from selenium.webdriver.common.by import By
from dunetuf.ews.EwsCapabilities import EwsCapability
import time
from dunetuf.copy.copy import Copy
from dunetuf.job.job import Job
from tests.copy.ews.copy_default_settings.copy_ews_combination import *
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
# Created by: pavan.gill@hp.com
# Date: 5/5/2023

def get_tray_data(cdm):
    cdm_deviceinfo = cdm.get(cdm.PRINTMODES_MEDIACONFIG_ENDPOINT)

    return cdm_deviceinfo["mediaConfigs"] 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if COLOR MODE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_default_copy_options_color_mode
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_color_mode
        +guid:cd2855c1-380d-4dba-8d02-425db986b30e
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanColorMode=BlackOnly

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_color_mode(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    # Only use string ids here that should appear on *all* products
    string_ids = {'color':'cColor', 'grayscale':'cChromaticModeGrayscale', 'blackAndWhite':'cBlackOnly'}
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "src/scan/colorMode":
            options=x['options']
            resultData=[]
            for optionValues in options:
                if optionValues.get('disabled', False) : 
                    if optionValues['disabled'] != "true":
                        resultData.append(optionValues['seValue'])
                else:
                    resultData.append(optionValues['seValue'])
    dropDownOptions = ews.driver.find_elements(By.XPATH, '//div[@id="colorMode-panel"]//mat-option//span')
    for index in range(0,len(dropDownOptions)):
        assert ews.get_string_translation(string_ids[resultData[index]]) == dropDownOptions[index].text
        helper.click('footer-defaultPrintFooter-button-apply')
        helper.ews.driver.refresh()    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if MEDIA TYPE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_default_copy_options_media_type
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_media_type
        +guid:5ae0aae5-b63b-43e7-ad3b-40b53164f2e5
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanOriginalPaperType=Blueprint & ScanOriginalPaperType=Translucent

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_media_type(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    # Only use string ids here that should appear on *all* products
    string_ids = {'whitePaper':'cColorWhite', 'blueprints':'cBlueprint', 'translucentPaper':'cPaperTypeTranslucent'}
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "src/scan/mediaType":
            options=x['options']
            resultData=[]
            for optionValues in options:
                if optionValues.get('disabled', False) : 
                    if optionValues['disabled'] != "true":
                        resultData.append(optionValues['seValue'])
                else:
                    resultData.append(optionValues['seValue'])
    dropDownOptions = ews.driver.find_elements(By.XPATH, '//div[@id="mediaType-panel"]//mat-option//span')
    for index in range(0,len(dropDownOptions)):
        assert ews.get_string_translation(string_ids[resultData[index]]) == dropDownOptions[index].text
        helper.click('footer-defaultPrintFooter-button-apply')
        helper.ews.driver.refresh()    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if PAPER SOURCE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_default_copy_options_paper_source
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_paper_source
        +guid:67d0d631-7dc5-47f8-be0f-52b97d0b1c9f
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & MediaInputInstalled=Main & MediaInputInstalled=MainRoll &MediaInputInstalled=SHEET
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_paper_source(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    string_ids = {'auto':'cAutomaticallySelect', 'main-roll':'cRoll', 'main':'cTray', 'top':'cSheet'}
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "dest/print/mediaSource":
            options=x['options']
            resultData=[]
            for optionValues in options:
                    resultData.append(optionValues['seValue'])
    dropDownOptions = ews.driver.find_elements(By.XPATH, '//div[@id="paperTray-panel"]//mat-option//span')
    for index in range(0,len(dropDownOptions)):
        assert ews.get_string_translation(string_ids[resultData[index]]) == dropDownOptions[index].text
        helper.click('footer-defaultPrintFooter-button-apply')
        helper.ews.driver.refresh()    

   
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if CONTENT TYPE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name:test_copy_ews_default_copy_options_content_type
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_content_type
        +guid:472781a3-2e92-4d2a-a736-51df52647e57
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanContentType=Image & ScanContentType=Lines & ScanContentType=Mixed

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_content_type(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    string_ids = {'lineDrawing':'cLines', 'mixed':'cMixed', 'image':'cImage'}
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "src/scan/contentType":
            options=x['options']
            resultData=[]
            for optionValues in options:
                    resultData.append(optionValues['seValue'])
    dropDownOptions = ews.driver.find_elements(By.XPATH, '//div[@id="contentType-panel"]//mat-option//span')
    for index in range(0,len(dropDownOptions)):
        assert ews.get_string_translation(string_ids[resultData[index]]) == dropDownOptions[index].text
        helper.click('footer-defaultPrintFooter-button-apply')
        helper.ews.driver.refresh()    


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if MARGIN TYPE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_default_copy_options_margin_type
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_margin_type
        +guid:694e24fd-6d08-4edd-93fb-b17c275e5294
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & Print=PrintMargins

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_margin_type(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    string_ids = {'clipContents':'cClipContentsByMargins', 'addToContents':'cAddToContents'}
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "dest/print/printMargins":
            options=x['options']
            resultData=[]
            for optionValues in options:
                    resultData.append(optionValues['seValue'])
    dropDownOptions = ews.driver.find_elements(By.XPATH, '//div[@id="printMargins-panel"]//mat-option//span')
    for index in range(0,len(dropDownOptions)):
        assert ews.get_string_translation(string_ids[resultData[index]]) == dropDownOptions[index].text
        helper.click('footer-defaultPrintFooter-button-apply')
        helper.ews.driver.refresh() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if NUMBER OF COPIES can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_default_copy_options_number_of_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_default_copy_options_number_of_copies
        +guid:020dc1bb-9a1b-4ebc-927e-4b27c943f662
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & Copy=NumberOfCopies

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_default_copy_options_number_of_copies(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    for x in cdm_deviceinfo['validators']:
        if x['propertyPointer'] == "uncollatedCopies":
            defaultValue=x['step']['value']
            helper.click('footer-defaultPrintFooter-button-apply')
            helper.ews.driver.refresh()  

            decrement= ews.driver.find_elements(By.ID, 'decrement')
            helper.click('footer-defaultPrintFooter-button-apply')
            helper.ews.driver.refresh()  

            increment= ews.driver.find_elements(By.ID, 'number-plus-button-copies')
            helper.click('footer-defaultPrintFooter-button-apply')
            helper.ews.driver.refresh()  


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if BACKGROUND NOISE REMOVAL can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_copy_default_job_background_noise_removal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_job_background_noise_removal
        +guid:2d3da8c0-3320-4bd2-a85e-2f13577d6cc4
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS &  DeviceFunction=Copy & ScanSettings=BackgroundNoiseRemoval
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_default_job_background_noise_removal(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)

    if  cdm_deviceinfo ['pipelineOptions']['imageModifications']['backgroundNoiseRemoval']:
        toggle = ews.driver.find_element(By.ID, 'backgroundNoiseRemoval-input')
        assert toggle.is_displayed()
        assert cdm_deviceinfo ['pipelineOptions']['imageModifications']['backgroundNoiseRemoval'] == toggle.get_attribute('aria-checked')
        ews.helper.click('backgroundNoiseRemoval-input')
        ews.helper.click('footer-config-job-options-button-apply')
    else:
        try:
            is_toggle_button_displayed = ews.driver.find_element(By.ID, 'backgroundNoiseRemoval').is_displayed()
        except:
            is_toggle_button_displayed = False
        assert is_toggle_button_displayed == False
    helper.ews.driver.refresh()  


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if BACKGROUND COLOR REMOVAL can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_copy_default_job_background_color_removal
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_job_background_color_removal
        +guid:170b8899-8cf2-4b67-beb3-f2fec62c7699
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanSettings=BackgroundColorRemoval
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_default_job_background_color_removal(helper,cdm, ews, configuration):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm.patch(cdm.JOB_TICKET_COPY, { 'src': {'scan': {"colorMode": "grayscale"}}})
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)

    if  cdm_deviceinfo['pipelineOptions']['imageModifications']['backgroundColorRemoval']:
        toggle = ews.driver.find_element(By.ID, 'backgroundColorRemoval-input')
        assert toggle.is_displayed()
        assert cdm_deviceinfo['pipelineOptions']['imageModifications']['backgroundColorRemoval'] == toggle.get_attribute('aria-checked')
        ews.helper.click('backgroundColorRemoval-input')
        ews.helper.click('footer-config-job-options-button-apply')
    else:
        try:
            is_toggle_button_displayed = ews.driver.find_element(By.ID, 'backgroundColorRemoval').is_displayed()
        except:
            is_toggle_button_displayed = False
        assert is_toggle_button_displayed == False
    helper.ews.driver.refresh() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if AUTO DESKEW can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_copy_default_job_auto_deskew
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_job_auto_deskew
        +guid:a000db7f-52aa-4ee7-90eb-ea0a4e163a57
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_default_job_auto_deskew(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)

    if  cdm_deviceinfo['src']['scan']['autoDeskew']:
        toggle = ews.driver.find_element(By.ID, 'autoDeskew-input')
        assert toggle.is_displayed()
        assert cdm_deviceinfo['src']['scan']['autoDeskew'] == toggle.get_attribute('aria-checked')
        ews.helper.click('autoDeskew-input')
        ews.helper.click('footer-config-job-options-button-apply')
    else:
        try:
            is_toggle_button_displayed = ews.driver.find_element(By.ID, 'autoDeskew').is_displayed()
        except:
            is_toggle_button_displayed = False
        assert is_toggle_button_displayed == False

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Checks if Include Margins can be set in COPY DEFAULTS EWS page && Checks if the changed value is reflected in the UI
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-191023
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework:TUF
    +test_classification:System
    +name: test_copy_ews_copy_default_job_fit_to_page_include_margin
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_job_fit_to_page_include_margin
        +guid:aeeedad7-5abe-4171-b348-180d15b7bdf6
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=CopyColor & Copy=FitToPage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ews_copy_default_job_fit_to_page_include_margin(helper,cdm, ews, spice, net):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)

    # EWS
    if  cdm_deviceinfo['pipelineOptions']['scaling']['fitToPageIncludeMargin']:
        toggle = ews.driver.find_element(By.ID, 'fitToPageIncludeMargin-input')
        assert toggle.is_displayed()
        assert cdm_deviceinfo['pipelineOptions']['scaling']['fitToPageIncludeMargin'] == toggle.get_attribute('aria-checked')
        ews.helper.click('fitToPageIncludeMargin-input')
        ews.helper.click('footer-config-job-options-button-apply')
        time.sleep(5)
        cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)
        assert cdm_deviceinfo['pipelineOptions']['scaling']['fitToPageIncludeMargin'] == "true"
    else:
        try:
            is_toggle_button_displayed = ews.driver.find_element(By.ID, 'fitToPageIncludeMargin').is_displayed()
        except:
            is_toggle_button_displayed = False
        assert is_toggle_button_displayed == False

    # UI
    logging.info("Go to Menu -> Copy -> Copy option list")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()

    logging.info("Verify the value displayed for fit to page include margin")
    copy_job_app.verify_copy_option_output_scale_fit_to_page_include_margin(True)

    logging.info("go back to home screen")
    spice.click_backButton()
    closeButton = spice.wait_for("#closeButton")
    closeButton.mouse_click()
    spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if EDGE TO EDGE can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:120
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_copy_default_job_edge_to_edge_scan
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_job_edge_to_edge_scan
        +guid:f96306e0-0a15-497e-8825-ee187b9919d0
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanSettings=EdgeToEdgeOutput
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_default_job_edge_to_edge_scan(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)

    if  cdm_deviceinfo['src']['scan']['edgeToEdgeScan']:
        toggle = ews.driver.find_element(By.ID, 'edgeToEdgeScan-input')
        second_toggle = ews.driver.find_element(By.ID, 'edgeToEdgeScan-input')
        third_toggle = ews.driver.find_element(By.ID, 'autoDeskew-input')
        assert toggle.is_displayed()
        assert cdm_deviceinfo['src']['scan']['edgeToEdgeScan'] == toggle.get_attribute('aria-checked')
        ews.helper.click('footer-config-job-options-button-apply')
    else:
        try:
            is_toggle_button_displayed = ews.driver.find_element(By.ID, 'edgeToEdgeScan').is_displayed()
        except:
            is_toggle_button_displayed = False
        assert is_toggle_button_displayed == False
    helper.ews.driver.refresh() 


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Checks if LIGHTER DARKER can be set in COPY DEFAULTS EWS page
    +test_tier:2
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-135965
    +timeout:400
    +asset:Copy
    +test_framework: TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ews_copy_default_lighter_darker
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_copy_default_lighter_darker
        +guid:7446f06f-4d99-484c-ae2f-c054d046ff05
        +dut:
            +type:Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & ScanSettings=Contrast
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_copy_default_lighter_darker(helper,cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)

    for val in range(2,10):
        ews.helper.select_lighter_darker(int(5))
        ews.helper.click('footer-config-job-options-button-apply')


@pytest.fixture(autouse=True)
def Initialize_Cleanup(ews, cdm, udw, spice, testname):
    # Test Initialize
    logging.info("[test][Initialize] START ========================================================")
    logging.info("[test][Initialize] testname(%s)", testname)
    spice.goto_homescreen()
    ews.home.load_home_page()
    logging.info("[test][Initialize] END ========================================================")

    yield [ews, cdm, udw, spice]

    # Test Cleanup
    logging.info("[test][Cleanup] START ========================================================")
    logging.info("[test][Cleanup] testname(%s)", testname)
    if testname == 'test_printer_features_change_feature_copy':
        logging.info("[test][Cleanup] set copyEnabled(true)")
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(
            cdm, cdm.COPY_CONFIGURATION_ENDPOINT, "copyEnabled", "true")
    if testname == 'test_printer_features_change_feature_colorcopy':
        is_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
        if is_supported:
            logging.info(
                "[test][Cleanup] set colorCopyEnabled(true), copyEnabled(true)")
            ews.security_app.printer_features_page.test_ews_modify_cdm_property(
                cdm, cdm.COPY_CONFIGURATION_ENDPOINT, "colorCopyEnabled", "true")
            ews.security_app.printer_features_page.test_ews_modify_cdm_property(
                cdm, cdm.COPY_CONFIGURATION_ENDPOINT, "copyEnabled", "true")
    if testname == 'test_printfromusb_ui_printer_features_change_feature':
        logging.info("[test][Cleanup] set printFromUsbEnabled(true)")
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(
            cdm, cdm.USB_HOST_CONFIGURATION, "printFromUsbEnabled", "true")
    if testname == 'test_printfromnetwork_ui_printer_features_change_feature':
        logging.info("[test][Cleanup] set networkFolderPrintEnabled(true)")
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(
            cdm, cdm.SMB_CDM_ENDPOINT, "networkFolderPrintEnabled", "true")
    if testname == 'test_printfrommyhome_ui_printer_features_change_feature':
        logging.info("[test][Cleanup] set homeFolderPrintEnabled(true)")
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(
            cdm, cdm.SMB_CDM_ENDPOINT, "homeFolderPrintEnabled", "true")
    
    spice.goto_homescreen()
    ews.home.load_home_page()
    logging.info("[test][Cleanup] END ========================================================")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Make sure that EWS enables and disables for Copy feature.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-61892
    +timeout: 500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name: test_printer_features_change_feature_copy
    +test:
        +title: test_printer_features_change_feature_copy
        +guid:4f57e11f-8135-4e45-833a-555b8f1ebc59
        +dut:
            +type: Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & EWS=PrinterFeatures
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_printer_features_change_feature_copy(ews, cdm, udw, spice, net):
    CDM_PROPERTY_COPY = "copyEnabled"
    CDM_PROPERTY_COLOR_COPY = "colorCopyEnabled"
    _feature_copy = "copyEnabled"

    logging.info("[test]START ========================================================")

    logging.info("[test]1.clear settings(uncheck) before starting this test-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COLOR_COPY, "false")
    ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COPY, "false")

    logging.info("[test]2.Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
    ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)

    logging.info("[test]3.Enable Copy feature-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_change_feature_from_disable2enable(_feature_copy)

    logging.info("[test]4.Verify if Copy app exists-----------------------------------------------")
    ews.security_app.printer_features_page.test_printer_features_verify_cp_copy_app_when_enabled(spice)

    logging.info("[test]5.Disable Copy feature-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_change_feature_from_enable2disable(_feature_copy)

    logging.info("[test]6.Verify if Copy app shows that the feature is disabled-----------------------------------------------")
    ews.security_app.printer_features_page.test_printer_features_verify_cp_copy_app_when_disabled(spice)

    logging.info("[test]7.Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
    ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)

    logging.info("[test]END ========================================================")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Make sure that EWS enables and disables for Color Copy feature.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-61892
    +timeout: 900
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name: test_printer_features_change_feature_colorcopy
    +test:
        +title: test_printer_features_change_feature_colorcopy
        +guid:6c9d396e-0fcb-412a-bdcf-099a67e95c03
        +dut:
            +type: Simulator
            +configuration: WebServices=EWS & DeviceFunction=Copy & PrintEngineMarking=Color & ScannerInput=Flatbed & EWS=PrinterFeatures
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""


def test_printer_features_change_feature_colorcopy(ews, cdm, udw, spice, net):
    CDM_PROPERTY_COPY = "copyEnabled"
    CDM_PROPERTY_COLOR_COPY = "colorCopyEnabled"
    _feature_copy = "copyEnabled"
    _feature_color_copy = "colorCopyEnabled"

    logging.info("[test]START ========================================================")

    logging.info("1. check if color is supported")
    is_supported = ews.security_app.printer_features_page.check_color_supported(cdm)
    if is_supported == False:
        logging.info("1. skip test - color is not supported.")
        return

    logging.info("1. run test - color is supported.")

    logging.info("[test]1.clear settings(uncheck) before starting this test-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COLOR_COPY, "false")
    ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COPY, "false")

    logging.info("[test]2.Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
    ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)

    logging.info("[test]3.Enable Copy feature-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_change_feature_from_disable2enable(_feature_copy)

    logging.info("[test]4.disable color Copy and check disable Color Mode feature----------------------------------------")
    ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COLOR_COPY, "false")
    ews.security_app.printer_features_page.test_printer_features_verify_cp_copy_app_not_visible_color_mode(spice, net)

    logging.info("[test]5.Enable color Copy feature----------------------------------------------------------------------")
    ews.security_app.printer_features_page.test_ews_change_feature_from_disable2enable(_feature_color_copy)

    logging.info("[test]6.Verify if Copy app exists-----------------------------------------------")
    ews.security_app.printer_features_page.test_printer_features_verify_cp_copy_app_when_enabled(spice)

    logging.info("[test]7.Disable Copy feature-----------------------------------------------")
    ews.security_app.printer_features_page.test_ews_change_feature_from_enable2disable(_feature_color_copy)
    ews.security_app.printer_features_page.test_ews_change_feature_from_enable2disable(_feature_copy)

    logging.info("[test]8.Verify if Copy app shows that the feature is disabled-----------------------------------------------")
    ews.security_app.printer_features_page.test_printer_features_verify_cp_copy_app_when_disabled(spice)

    logging.info("[test]9.Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
    ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)

    logging.info("[test]END ========================================================")

"""     
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that user defined options are coming in the copy default options in paper type
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-153611
    +timeout:120
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +test_classification:System
    +name:test_ews_copy_user_defined_option
    +test:
        +title:test_ews_copy_user_defined_option
        +guid:c7a6f00e-7ece-11ee-a12c-27619b076faa
        +dut:
            +type:Emulator
            +configuration:MediaType=UserDefined
     
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ews_copy_user_defined_option(ews):
    # Retrieve tray data from EWS
    result_data = get_tray_data(ews.cdm)
    # Filter data for user-defined options
    filtered_data = [item for item in result_data if item['mediaType'].startswith("com.hp.usertype-")]

    # Extract all "userDefinedName" values from filtered_data
    user_defined_names = [item['userDefinedName'] for item in filtered_data if item['mediaTypeVisibleEnabled'] == 'true' ]

    # Load the print options page
    ews.load("/copy/defaultJobOptions")
    ews.helper.wait_for_loading_complete(3)

    # Click on the paper type dropdown
    dropdown_option = ews.get_element_by_id('paperType')
    dropdown_option.click()

    # Extract text content of dropdown options
    option_elements = ews.driver.find_elements(By.XPATH, "//span[@class='mat-option-text']")
    option_elements_text = [actual_item.get_attribute('textContent').strip() for actual_item in option_elements]
    

    # assert the text in user_defined_names and option_elements_text
    for option_text in user_defined_names:
        assert option_text in option_elements_text

"""     
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify the booklet Format  
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-215185
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_ews_copy_booklet_format
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_ews_copy_booklet_format
        +guid:4cdeb84e-9f97-11ef-88f3-9f4c907df3de
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat
              & CopyBooklet=BookletFormatOnOff
     
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ews_copy_booklet_format(ews, helper):
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    logging.info("set staple values as topRightOnePointAngled")
    value = 'Fit to Page'
    helper.select_from_dropdown("outputScale", value)
    booklet_format = ews.helper.wait_for_element_visible((By.ID, "bookletFormat-name")).is_displayed()
    assert booklet_format == True   

    ews.helper.wait_for_element_visible((By.ID, "outputScale"))
    value = 'Custom'
    helper.select_from_dropdown("outputScale", value)
    helper.click('footer-config-job-options-button-apply')

    helper.navigate_to_url(wait_for_card = True)
    ews.helper.wait_for_element_visible((By.ID, "outputScale"))
    try:
        # Try to find the element by ID
        booklet_format = ews.driver.find_element(By.ID, "bookletFormat-name").is_displayed()
        assert booklet_format == False
        is_visible = True
    except NoSuchElementException:
        is_visible = False

"""     
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that scan mode dropdown options are coming in the copy default options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-196072
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ews_scan_mode
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_scan_mode
        +guid:3577b86e-3dcb-11ef-832c-53ff4276f8f1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
     
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_scan_mode(ews, cdm, helper):
    
    # Load the copy default option page
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)
    
    addPages = ews.get_string_translation('cStandardDocumentAddPages')
    standard = ews.get_string_translation('cStandardDocumentLabel')

    #scan mode title check
    title = ews.get_element_by_id('scanCaptureMode-name')
    assert title.text == ews.get_string_translation('cScanMode')

    # Click on the scan mode dropdown and selecting values
    helper.select_from_dropdown('scanCaptureMode', addPages)
    helper.assert_field_text('scanCaptureMode', addPages)

    #click apply button
    ews.helper.click('footer-config-job-options-button-apply')

    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    helper.assert_field_text('scanCaptureMode', addPages)
    helper.select_from_dropdown('scanCaptureMode', standard)

    #click cancel button
    ews.helper.click('footer-config-job-options-button-cancel')

    helper.select_from_dropdown('scanCaptureMode', standard)
    ews.helper.click('footer-config-job-options-button-apply')

"""     
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that scan mode dropdown options are coming in the copy default options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-196072
    +timeout:180
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ews_scan_book_mode
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_scan_book_mode
        +guid:104ec572-58cf-11ef-8b0a-5ba392035eb9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt
     
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_scan_book_mode(ews, cdm, helper):
    
    # Load the copy default option page
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)
    
    book = ews.get_string_translation('cBookMode')

    #scan mode title check
    title = ews.get_element_by_id('scanCaptureMode-name')
    assert title.text == ews.get_string_translation('cScanMode')

    # Click on the scan mode dropdown and selecting values
    helper.select_from_dropdown('scanCaptureMode', book)
    helper.assert_field_text('scanCaptureMode', book)

    #click apply button
    ews.helper.click('footer-config-job-options-button-apply')

    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    helper.assert_field_text('scanCaptureMode', book)
    
    #click cancel button
    ews.helper.click('footer-config-job-options-button-cancel')

    helper.select_from_dropdown('scanCaptureMode', book)
    ews.helper.click('footer-config-job-options-button-apply')

"""     
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that scan mode dropdown options are coming in the copy default options
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-196072
    +timeout:260
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ews_scan_two_sided_mode
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_scan_two_sided_mode
        +guid:c4fa722e-74fd-11ef-9b4c-eb8cc22b6a70
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ScanSettings=PromptforAdditionalPages
     
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_scan_two_sided_mode(ews, cdm, helper):
    
    # Load the copy default option page
    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    cdm_deviceinfo = cdm.get(cdm.JOB_TICKET_COPY)
    
    bothside = ews.get_string_translation('cIdScanBothSides')
    backside = ews.get_string_translation('cIdScanBackSide')
    standard = ews.get_string_translation('cStandardDocumentLabel')

    #scan mode title check
    title = ews.get_element_by_id('scanCaptureMode-name')
    assert title.text == ews.get_string_translation('cScanMode')

    # Click on the scan mode dropdown and selecting values for bothside
    helper.select_from_dropdown('scanCaptureMode', bothside)
    helper.assert_field_text('scanCaptureMode', bothside)

    #click apply button
    ews.helper.click('footer-config-job-options-button-apply')

    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    helper.assert_field_text('scanCaptureMode', bothside)

    # Click on the scan mode dropdown and selecting values for back side
    helper.select_from_dropdown('scanCaptureMode', backside)
    helper.assert_field_text('scanCaptureMode', backside)

    #click apply button
    ews.helper.click('footer-config-job-options-button-apply')

    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    helper.assert_field_text('scanCaptureMode', backside)
    
    # Click on the scan mode dropdown and selecting values to patch back to default
    helper.select_from_dropdown('scanCaptureMode', standard)
    helper.assert_field_text('scanCaptureMode', standard)

    #click apply button
    ews.helper.click('footer-config-job-options-button-apply')

    helper.load_and_wait(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT, wait_for_card = True)
    helper.assert_field_text('scanCaptureMode', standard)
  
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the Folding Styles dropdown in "default copy options" page EWS.
    +test_tier: 1
    +is_manual:False
    +reqid:DUNE-214981
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_ews_job_copy_default_job_options_folding_styles
    +test:
        +title:test_ews_job_copy_default_job_options_folding_styles
        +guid:4f336474-cd72-11ef-bd32-ff72a8de4672
        +dut:
            +type:Simulator
            +configuration:CopyOutputDestination=Folder & CopySettings=FoldingStyle
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ews_job_copy_default_job_options_folding_styles(cdm, ews):
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    ews.helper.wait_for_loading_complete()

    # Select the folder as the output destination
    ews.helper.select_from_dropdown('mediaDestination', 'Folder')

    cdm_constraints = cdm.get(cdm.JOB_TICKET_COPY_CONSTRAINTS)
    cdm_finisher_configuration = cdm.get(cdm.MEDIA_FINISHER_CONFIGURATION)

    # Get posibles values for foldingStyleId from the constraints
    for x in cdm_constraints['validators']:
        if x['propertyPointer'] == "dest/print/foldingStyleId":
            options=x['options']
            folding_style_id_options=[]
            for option_values in options:
                folding_style_id_options.append(option_values['iValue'])

    # Create a map of localization string ids and folding style ids from the finisherConfiguration
    localization_string_ids_map = {}
    for standard_folding_styles_supported in cdm_finisher_configuration['folders'][0]['standardFoldingStylesSupported']:
        localization_string_ids_map[standard_folding_styles_supported['foldingStyleName']]=standard_folding_styles_supported['foldingStyleId']

    # Get the dropdown options strings shown when clicking the dropdown
    ews.helper.wait_for_then_click("foldingStyleId")
    dropdown_options = ews.driver.find_elements(By.XPATH, "//mat-option")

    assert  len(dropdown_options)>0, "There are no Folding Styles in the EWS 'copy < default copy options'"

    for index in range(0,len(dropdown_options)):
        # Check if the string shown in the dropdown exist in the localization_string_ids_map
        assert  localization_string_ids_map.get(dropdown_options[index].text,'Not found') !='Not found', "The string shown in the dropdown is not in the localization_string_ids_map"

        # Check that the id is in the constraints and remove it; Consequently, it will fail if there are duplicates
        assert  localization_string_ids_map[dropdown_options[index].text] in folding_style_id_options, "The id is not in the constraints"
        folding_style_id_options.remove(localization_string_ids_map[dropdown_options[index].text])