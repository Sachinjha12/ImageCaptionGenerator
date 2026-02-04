import logging
import copy
from tests.copy.copy_ews_combination import *
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_A4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_A4
        +guid:4748b4b0-2cf8-43dd-91c0-02657c060386
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=3x5
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_A4(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "iso_a4_210x297mm"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as A4(210x297mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_A4)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()      

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_SEF_A4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_SEF_A4
        +guid:e412129e-9da4-43bf-afd1-2f96a722107a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=3x5
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_SEF_A4(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a4_210x297mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF A4(210x297mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_SEF_A4)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)

    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_A5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_A5
        +guid:a79875a3-ef63-451b-8dea-33bebc09b47b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=A5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_A5(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "iso_a5_148x210mm"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as A5(148x210mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_A5)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_SEF_A5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_SEF_A5
        +guid:70fef6e3-9b3d-47fb-ba7f-61e54289abbf
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=A5
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_SEF_A5(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "com.hp.ext.mediaSize.iso_a5_148x210mm.rotated"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF A5(148x210mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_SEF_A5)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_B6_Jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_B6_Jis
        +guid:682d8669-8cf6-4a44-bccd-6cd33437890d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=B6-JIS

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_B6_Jis(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "jis_b6_128x182mm"
        #setting the size of the display is inconsistent with that in the data
        ews_copy_app = ews.copy_ews_app
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as B6(JIS)(128x182)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_B6_Jis)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_b5_jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_b5_jis
        +guid:d01460a4-1b20-4a68-a9e2-b1d89d120bfe
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=B5-JIS

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_b5_jis(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings_b5_jis = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings_b5_jis["src"]["scan"]["mediaSize"] = "jis_b5_182x257mm"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as jis_b5_182x257mm")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_combi_original_size_b5_jis)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings_b5_jis)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_SEF_b5_jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_SEF_b5_jis
        +guid:108864d2-ad3e-4ea0-970c-7479f40df523
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=B5-JIS
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_SEF_b5_jis(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings_SEF_b5_jis = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings_SEF_b5_jis["src"]["scan"]["mediaSize"] = "com.hp.ext.mediaSize.jis_b5_182x257mm.rotated"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF_jis_b5_182x257mm")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_combi_original_size_SEF_b5_jis)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings_SEF_b5_jis)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_double_postcard_jis
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_double_postcard_jis
        +guid:7747740c-0af8-469d-8f76-9e962f7f269c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=DoubleJapanPostcardRotated

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_double_postcard_jis(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "jpn_oufuku_148x200mm"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as double postcard (JIS)(148x200)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_double_postcard_jis)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_executive
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_executive
        +guid:c6310548-0151-44ff-b53d-202da8a6d186
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=Executive

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_executive(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "na_executive_7.25x10.5in"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as Executive (7.25x10.5 in.)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_executive)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_five_multiply_eight_in
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_five_multiply_eight_in
        +guid:748fcba4-05d3-45be-b6c1-bac19cbe8c31
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=5x8

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_five_multiply_eight_in(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "na_index-5x8_5x8in"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as (5x8_in)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_five_multiply_eight)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy__ews_originalsize_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy__ews_originalsize_letter
        +guid:26c69535-eaad-4a6c-ac21-9aaf231e1ad2
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=Letter
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy__ews_originalsize_letter(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "na_letter_8.5x11in"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as letter(8.5x11 in.)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_letter)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_SEF_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_SEF_letter
        +guid:523b3f17-b715-469b-8dd2-a2eaee178486
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineFormat=A3 & FlatbedMediaSize=Letter & ScannerInput=AutomaticDocumentFeeder & ScannerInput=Flatbed
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_SEF_letter(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "com.hp.ext.mediaSize.na_letter_8.5x11in.rotated"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as SEF_letter(8.5x11 in.)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_SEF_letter)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_16k_195_270
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_16k_195_270
        +guid:eb3c826b-28df-4b67-8947-62c8be113370
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=16K195x270mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_16k_195_270(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "om_16k_195x270mm"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as 16K(195x270mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_16K_195_270)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_16k_197_273
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_16k_197_273
        +guid:e4d2369a-ea4f-41f7-9b4b-dfe0264fb084
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=16K197x273mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_16k_197_273(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "roc_16k_7.75x10.75in"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as 16K(197x273mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_16K_197_273)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set original size and verify values by cdm
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
    +name:test_copy_ews_originalsize_statement
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_statement
        +guid:4b6a130c-b59d-4d7b-8ea6-f430cb74cd2e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=Statement

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_statement(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings["src"]["scan"]["mediaSize"] = "na_invoice_5.5x8.5in"

        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as statement(8.5x5.5 in.)")
        ews_copy_app.edit_copy_ews_setting(job_copy_ews_options= job_copy_option_combi_original_size_statement)
        ews_copy_app.click_ews_copy_page_apply_button()
        
        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings)
    finally:
        logging.info("Restore set values")
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
        ews.close_browser()


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
    +name:test_copy_ews_originalsize_16K_184x260
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews_originalsize_16K_184x260
        +guid:0bf834fc-2676-4638-99cf-fe28ed1d1de6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy&FlatbedMediaSize=16K184x260mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews_originalsize_16K_184x260(ews):
    ews_copy_app = ews.copy_ews_app
    default_value = ews_copy_app.get_job_copy_response()
    try:
        update_expected_settings_envelop_10 = ews_copy_app.make_checking_field_with_cdm_on_ews_job_copy(default_value)
        update_expected_settings_envelop_10['dest']['print']['mediaSize'] = "om_16k_184x260mm"
        logging.info("load the job copy page")
        ews_copy_app.load_jobs_copy_page()
        logging.info("set original size values as 16K (184x260 mm)")
        ews_copy_app.edit_copy_ews_setting(job_copy_option_combi_original_16K_184x260)
        ews_copy_app.click_ews_copy_page_apply_button()

        logging.info("check the values by cdm")
        ews_copy_app.check_with_cdm_on_ews_job_copy(update_expected_settings_envelop_10)

    finally:
        logging.info("Restore set values")
        ews.close_browser()
        ews_copy_app.recovery_default_value_by_cdm_on_job_copy(default_value)
