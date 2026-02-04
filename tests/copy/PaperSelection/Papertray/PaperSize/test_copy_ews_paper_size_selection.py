import logging
import copy
from tests.copy.copy_ews_combination import *
from dunetuf.job.job import Job
from selenium.webdriver.common.by import By

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_SEF_A4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_SEF_A4
        +guid:89a644d5-a670-452e-845a-af99f29b224e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=3x5
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_papersize_SEF_A4(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set paper size values as SEF A4(210x297mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_SEF_A4)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_SEF_A5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_SEF_A5
        +guid:6e61d516-d396-4281-8cfa-fcf1932e4539
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=A5 & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_papersize_SEF_A5(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a5_148x210mm.rotated"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set paper size values as SEF A5(148x210mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_SEF_A5)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_SEF_b5_jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_SEF_b5_jis
        +guid:426821f5-03f5-45d5-9610-094b83f7ca5f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=B5-JIS
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_papersize_SEF_b5_jis(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings_SEF_b5_jis = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings_SEF_b5_jis["dest"]["print"]["mediaSize"] = "com.hp.ext.mediaSize.jis_b5_182x257mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF_jis_b5_182x257mm")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_combi_paper_size_SEF_b5_jis)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings_SEF_b5_jis)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-85425
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_SEF_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_SEF_letter
        +guid:d8b14eb7-1022-4c99-9068-f906d5cfec75
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=Letter
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_papersize_SEF_letter(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "com.hp.ext.mediaSize.na_letter_8.5x11in.rotated"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF_letter(8.5x11 in.)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_SEF_letter)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143686
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_match_original
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_match_original
        +guid:39d70f8f-a87a-4fcd-a2a5-74e26b338384
        +dut:
            +type:Simulator
            +configuration: DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_papersize_match_original(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "any"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set match_original size")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_match_original)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
            
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143690
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_custom_aver
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_papersize_custom_aver
        +guid:0230dfa4-2555-4160-b4b2-eef8f00b6c4c
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_papersize_custom_aver(ews, cdm):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "custom"

        job_ticket_constraint_value = get_constraints_value(ews_copy_app, cdm)
        custom_x_aver, custom_y_aver = get_custom_constraints_value(job_ticket_constraint_value, "aver")

        update_expected_settings["dest"]["print"]["customMediaXFeedDimension"] = custom_x_aver
        update_expected_settings["dest"]["print"]["customMediaYFeedDimension"] = custom_y_aver

        custom_x_aver = dpiToInch(custom_x_aver)
        custom_y_aver = dpiToInch(custom_y_aver)

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set custom size")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom)

        if(ews.driver.find_element(By.ID, "displayUnitOfMeasure").text!="Inches"):
            ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_unit_inches)

        job_copy_option_combi_paper_size_custom_value = {
        CopyEwsOptionsKey.custom_media_x_feed_dimension: str(custom_x_aver),
        CopyEwsOptionsKey.custom_media_y_feed_dimension: str(custom_y_aver)
        }

        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom_value)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143690
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_custom_min
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_papersize_custom_min
        +guid:c3f558d3-022d-4a44-917b-2f2cba8bb519
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_papersize_custom_min(ews, cdm):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "custom"

        job_ticket_constraint_value = get_constraints_value(ews_copy_app, cdm)
        custom_x_min, custom_y_min = get_custom_constraints_value(job_ticket_constraint_value, "min")

        update_expected_settings["dest"]["print"]["customMediaXFeedDimension"] = custom_x_min
        update_expected_settings["dest"]["print"]["customMediaYFeedDimension"] = custom_y_min

        custom_x_min = dpiToInch(custom_x_min)
        custom_y_min = dpiToInch(custom_y_min)

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set custom size")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom)

        if(ews.driver.find_element(By.ID, "displayUnitOfMeasure").text!="Inches"):
            ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_unit_inches)

        job_copy_option_combi_paper_size_custom_value = {
        CopyEwsOptionsKey.custom_media_x_feed_dimension: str(custom_x_min),
        CopyEwsOptionsKey.custom_media_y_feed_dimension: str(custom_y_min)
        }
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom_value)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143690
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_custom_max
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_papersize_custom_max
        +guid:25cc6869-aae5-496c-80ac-163db3a8b332
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_papersize_custom_max(ews, cdm):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "custom"

        job_ticket_constraint_value = get_constraints_value(ews_copy_app, cdm)
        custom_x_max, custom_y_max = get_custom_constraints_value(job_ticket_constraint_value, "max")

        update_expected_settings["dest"]["print"]["customMediaXFeedDimension"] = custom_x_max
        update_expected_settings["dest"]["print"]["customMediaYFeedDimension"] = custom_y_max

        custom_x_max = dpiToInch(custom_x_max)
        custom_y_max = dpiToInch(custom_y_max)

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set custom size")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom)

        if(ews.driver.find_element(By.ID, "displayUnitOfMeasure").text!="Inches"):
            ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_unit_inches)

        job_copy_option_combi_paper_size_custom_value = {
        CopyEwsOptionsKey.custom_media_x_feed_dimension: str(custom_x_max),
        CopyEwsOptionsKey.custom_media_y_feed_dimension: str(custom_y_max)
        }
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom_value)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set paper size and verify values by cdm
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143690
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews_papersize_custom_mm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ews_papersize_custom_mm
        +guid:2cd165bf-a985-45d8-a0ab-a9bbcb808c3f
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_papersize_custom_mm(ews, cdm):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["dest"]["print"]["mediaSize"] = "custom"

        job_ticket_constraint_value = get_constraints_value(ews_copy_app, cdm)
        custom_x_aver, custom_y_aver = get_custom_constraints_value(job_ticket_constraint_value, "aver")

        custom_x_aver_mm = dpiToMm(custom_x_aver)
        custom_y_aver_mm = dpiToMm(custom_y_aver)
        custom_x_aver = mmToDpi(custom_x_aver_mm)
        custom_y_aver = mmToDpi(custom_y_aver_mm)

        update_expected_settings["dest"]["print"]["customMediaXFeedDimension"] = custom_x_aver
        update_expected_settings["dest"]["print"]["customMediaYFeedDimension"] = custom_y_aver

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set custom size")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom)

        if(ews.driver.find_element(By.ID, "displayUnitOfMeasure").text!="Millimeters"):
            ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_unit_millimeters)

        job_copy_option_combi_paper_size_custom_value = {
        CopyEwsOptionsKey.custom_media_x_feed_dimension: str(custom_x_aver_mm),
        CopyEwsOptionsKey.custom_media_y_feed_dimension: str(custom_y_aver_mm)
        }
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_paper_size_custom_value)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

def get_constraints_value(ews_copy_app, cdm):
    body = { 'src': {'scan':{}}, 'dest': {'print':{}} }
    rep = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert 200 <= rep.status_code < 300
    ticket_id = rep.json()['ticketId']

    result = ews_copy_app.get_job_ticket_constraints_response(ticket_id)

    return result

def get_custom_constraints_value(job_ticket_constraint_value, value):
    for item in job_ticket_constraint_value:
        if item["propertyPointer"] == "dest/print/customMediaXFeedDimension":
            custom_x = item
        elif item["propertyPointer"] == "dest/print/customMediaYFeedDimension":
            custom_y = item    

    custom_x_min = custom_x["minDouble"]["value"]
    custom_x_max = custom_x["maxDouble"]["value"]
    custom_x_aver = round((custom_x_min + custom_x_max) / 2 / 100) * 100

    custom_y_min = custom_y["minDouble"]["value"]
    custom_y_max = custom_y["maxDouble"]["value"]
    custom_y_aver = round((custom_y_min + custom_y_max) / 2 / 100) * 100

    if value == "aver":
        return custom_x_aver, custom_y_aver
    elif value == "min":
        return custom_x_min, custom_y_min
    elif value == "max":
        return custom_x_max, custom_y_max

def mmToDpi(value):
    return round((round(value / 10 / 2.54 * 100)) * 100, 1)
    #2.54 = cm per inch
    
def dpiToMm(value):
    return round(value / 10000 * 10 * 2.54, 1)

def dpiToInch(value):
    return round(value / 10000, 2)
