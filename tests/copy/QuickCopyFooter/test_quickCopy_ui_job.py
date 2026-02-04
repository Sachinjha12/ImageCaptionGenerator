from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.copy.copy import *
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify number of copies of spin box is equal to the no of copies in job
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickcopy_footer_validate_spinbox_copies_match_job_copies
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickcopy_footer_validate_spinbox_copies_match_job_copies
        +guid:0f144642-6ab6-4a7c-bb89-c38a93b4bf49
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_quickcopy_footer_validate_spinbox_copies_match_job_copies(setup_teardown_with_copy_job,spice,job,cdm,udw,net,configuration):
    try: 
        job.bookmark_jobs()
        cp_app = spice.copy_ui()
        copy_Count=20
        cp_app.set_number_of_footer_spinBox_copies(copy_Count)
        cp_app.perform_copy_from_homescreen_footer()
        Copy(cdm, udw).validate_settings_used_in_copy(number_of_copies=copy_Count)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
      
        
    finally:
        cp_app.set_number_of_footer_spinBox_copies(1)
        spice.cleanSystemEventAndWaitHomeScreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify copy button is disabled when copy is executing
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickcopy_footer_validate_copy_button_disabled_when_copy_starts
    +test:
        +title:test_copy_ui_quickcopy_footer_validate_copy_button_disabled_when_copy_starts
        +guid:8a5ed8be-73ba-493c-997d-37081a2f5411
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_quickcopy_footer_validate_copy_button_disabled_when_copy_starts(setup_teardown_with_copy_job,spice,net,configuration,udw):

    try:
        cp_app = spice.copy_ui()
        cp_app.perform_copy_from_homescreen_footer()
        cp_app.check_footer_copy_start_button_disabled()
        cp_app.wait_for_copy_status_toast(net,configuration, message='Complete')

    finally:
        spice.cleanSystemEventAndWaitHomeScreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify toast message when copy is executing using homescreen copy footer
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickcopy_footer_validate_toast_message_when_copy_starts
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickcopy_footer_validate_toast_message_when_copy_starts
        +guid:b840a5fa-1d85-11ef-8a95-9fc6ee9f8992
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""       
def test_copy_ui_quickcopy_footer_validate_toast_message_when_copy_starts(setup_teardown_with_copy_job,spice,net,configuration,udw):
        
    try:
        cp_app = spice.copy_ui()
        copy_Count=20
        cp_app.set_number_of_footer_spinBox_copies(copy_Count)
        cp_app.perform_copy_from_homescreen_footer()
        cp_app.wait_for_copy_status_toast(net,configuration, message='Copying')
        cp_app.wait_for_copy_status_toast(net,configuration, message='Complete')
    finally:
        cp_app.set_number_of_footer_spinBox_copies(1)
        spice.cleanSystemEventAndWaitHomeScreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify toast message when copy is executing using homescreen copy footer
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:390
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickCopy_footer_validate_feature_enable_and_disable_from_ews
    +test:
        +title:test_copy_ui_quickCopy_footer_validate_feature_enable_and_disable_from_ews
        +guid:91c04e66-2342-4fa8-8696-8ec7db222c1a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer & EWS=PrinterFeatures
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""       
def test_copy_ui_quickCopy_footer_validate_feature_enable_and_disable_from_ews(setup_teardown_with_copy_job,ews,cdm,spice,net,configuration,udw):
    CDM_PROPERTY_COPY = "copyEnabled"
    _feature_copy = "copyEnabled"
    try:
        logging.info("START ========================================================")

        logging.info("clear settings(uncheck) before starting this test-----------------------------------------------")
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COPY, "false")

        logging.info("Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
        ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)

        logging.info("Enable Copy feature-----------------------------------------------")
        ews.security_app.printer_features_page.test_ews_change_feature_from_disable2enable(_feature_copy)

        logging.info("Verify if QuickCopy exists-----------------------------------------------")
        ews.security_app.printer_features_page.test_printer_features_verify_cp_quick_copy_state(spice,True)

        logging.info("Disable Copy feature-----------------------------------------------")
        ews.security_app.printer_features_page.test_ews_change_feature_from_enable2disable(_feature_copy)

        logging.info("Verify that QuickCopy is disabled-----------------------------------------------")
        ews.security_app.printer_features_page.test_printer_features_verify_cp_quick_copy_state(spice,False)

        logging.info("Verify if Copy default job option page shows 'Feature Disabled' message-----------------------------------------------")
        ews.security_app.printer_features_page.verify_feature_disable_status_box(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    finally:
        ews.security_app.printer_features_page.test_ews_modify_cdm_property(cdm, cdm.COPY_CONFIGURATION_ENDPOINT, CDM_PROPERTY_COPY, "true")
