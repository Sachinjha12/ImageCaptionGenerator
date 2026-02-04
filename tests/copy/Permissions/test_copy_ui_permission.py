import logging, logging.config
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
import pytest
import sys
import time

import UiPermissionsTestHelper
from tests.security.accountManagement.WindowsAuth.WindowsAuthTestHelper import WindowsAuthTestHelper


DEVICEUSER_ROLE_USER = "a69a546c-dd68-4e4b-8302-97cd6471a0a4"
DEVICEUSER_ROLE_ADMIN = "42e5e2d7-6c01-42b8-b086-ee8a1a2c25de"
GuestRoleGuid = "0a52b510-5db2-49f2-b95d-7f5c37c50235"
PermissionCopy = "ef92c290-8fa5-4403-85bc-f6becc86b787"
PermissionCopyColor = "af9ca74f-ce78-4a06-89b5-dd7094fbac42"


# Disable loggers for modules above (uncomment to apply)
"""
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True
})
"""

@pytest.fixture
def setup_teardown(udw,cdm, spice, ui_permissions_test_setup_teardown):
    udw.mainUiApp.KeyHandler.setKeyPress("HOME")
        
    
    # Run the test
    logging.info("Executing test... ")
    yield {"cdm": cdm, "spice": spice,"udw":udw, "ui_permissions": ui_permissions_test_setup_teardown}
    logging.info("Test exited! Returning to fixture...")

    logging.info("Starting test cleanup")
    udw.mainUiApp.KeyHandler.setKeyPress("HOME")
    if cdm.device_user.get_device_users_count() > 0:
        cdm.device_user.deleteallusers()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the RBAC permissions in the CopyApp with UI TestFramework
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-78676
    +timeout:2000
    +asset:Security
    +delivery_team:FWsolns
    +feature_team:Security
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_permission_copy_app
    +test:
        +title:test_permission_copy_app
        +guid:8b56f1b1-f0d0-4b81-a013-85e0708ecb59
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & Authentication=WindowsAuthentication & Authentication=LDAP & Authentication=Sign-in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_permission_copy_app(setup_teardown):
    """
    Test Copy permission
    """
    ui_permissions = setup_teardown["ui_permissions"]
    testname = sys._getframe().f_code.co_name
    logging.info(f"BEGINNING TEST: {testname}")

    # Run the standard test procedure
    ui_permissions.permission_test_procedure(PermissionCopy) # Send to Email->To Field

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the CopyJob RBAC permissions in the CopyApp with print user locked
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-78676
    +timeout:1000
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_permissions_printerUserLocked_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_permissions_printerUserLocked_subject
        +guid:28ece243-a3aa-4bd8-a323-fa2a176d8579
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & Authentication=Sign-in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_permissions_printerUserLocked_subject(spice,cdm,udw,job,ews,net):
    try:
        cdm.device_user.create_user('tester', '', 'Test@13579', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)

        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,DEVICEUSER_ROLE_USER,False)

        logging.info("Step 1: Enter valid credentials")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        
        # Go to CopyApp
        copy_job_app = spice.copy_ui()
        copyApp = copy_job_app.get_copy_app()
        copyApp.mouse_click()
        time.sleep(5)

        #time.sleep(3)
        #spice.goto_homescreen()

        spice.signIn.verifyPermissionEnforced(expected = False)
        spice.copy_ui().goto_menu_mainMenu()
        spice.signIn.goto_universal_sign_in("Sign Out")
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,GuestRoleGuid,True)
        logging.info("Step 2: Re sign in ")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        time.sleep(5)
        spice.signIn.goto_universal_sign_in("Sign Out")
        #spice.signIn.cleanup("user", "success")

    finally:  
        cdm.device_user.deleteallusers()
        #spice.signIn.cleanup("user", "success")   
        #cdm.device_user.delete_user("tester")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the CopyColor RBAC permissions in the CopyApp with print user locked
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-78676
    +timeout:1000
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_color_ui_permissions_printerUserLocked_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_color_ui_permissions_printerUserLocked_subject
        +guid:1b269878-1fa1-42fb-abfd-8a76ea6afbde
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & Authentication=Sign-in & Copy=GrayScale
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_ui_permissions_printerUserLocked_subject(spice,cdm,udw,job,ews,net):
    try:
        cdm.device_user.create_user('tester', '', 'Test@13579', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)

        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopyColor,DEVICEUSER_ROLE_USER,False)

        logging.info("Step 1: Enter valid credentials")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        
        try:
            spice.status_center.collapse()
        except:
            pass

        # Go to Copy options
        copy_job_app = spice.copy_ui()
        copyApp = copy_job_app.get_copy_app()
        copyApp.mouse_click()
        time.sleep(5)

        # Verify if Grayscale is selected in ColorMode
        copy_job_app.verify_copy_landing_selected_option(net, "color", "grayscale")
    
    finally:
        spice.copy_ui().goto_menu_mainMenu()
        spice.signIn.goto_universal_sign_in("Sign Out")
        cdm.device_user.deleteallusers()
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopyColor,GuestRoleGuid,True)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the QuickCopyJob RBAC permissions with print user locked
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:700
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickCopy_footer_permissions_printerUserLocked_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickCopy_footer_permissions_printerUserLocked_subject
        +guid:98df5a9c-1d8c-11ef-be27-2f2ca2d25644
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
""" 
def test_copy_ui_quickCopy_footer_permissions_printerUserLocked_subject(spice,cdm,udw,job,ews,net):
    try:
        cdm.device_user.create_user('tester', '', 'Test@13579', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)

        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,DEVICEUSER_ROLE_USER,False)

        logging.info("Step 1: Enter valid credentials")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        
        # Go to CopyApp
        copy_job_app = spice.copy_ui()
        #extend the test case to be run on widget also
        copyApp = copy_job_app.perform_copy_from_homescreen_footer()
        time.sleep(5)

        #time.sleep(3)
        #spice.goto_homescreen()

        spice.signIn.verifyPermissionEnforced(expected = False)
        #spice.signIn.cleanup("user", "success")

    finally:     
        #spice.signIn.cleanup("user", "success")   
        spice.goto_homescreen()
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,DEVICEUSER_ROLE_USER,True)
        spice.goto_homescreen()
        spice.signIn.goto_universal_sign_in("Sign Out")
        cdm.device_user.deleteallusers()
        #spice.signIn.cleanup("user", "success")   
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,GuestRoleGuid,True)
        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_sign_in_method("admin", "user")
        spice.signIn.enter_creds(True, "admin", "12345678")
        spice.sign_in_app.verify.welcome_user_toast_message("admin")
        spice.goto_homescreen()
        spice.signIn.goto_universal_sign_in("Sign Out")
        #cdm.device_user.delete_user("tester")
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the CopyJob RBAC permissions in the CopyApp with print user allowed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-78676
    +timeout:1000
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_permissions_printerUserAllowed_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_permissions_printerUserAllowed_subject
        +guid:43e1fbca-0375-4ef9-a554-092111a2edd0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & Authentication=Sign-in
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_permissions_printerUserAllowed_subject(setup_teardown):
    spice = setup_teardown["spice"]
    cdm = setup_teardown["cdm"]
    password = "Pass123test"

    logging.info("Step 1: Create device user")
    cdm.device_user.set_admin_as_default_signin()
    user_name = "tester"
    display_name = "displayname1"
    cdm.device_user.create_user(
        user_name,
        "",
        password,
        display_name,
        "user1@email.com",
        "networkuser1",
        DEVICEUSER_ROLE_USER)

    try:

       logging.info("Step 3: Enter valid credentials")
       spice.signIn.goto_universal_sign_in("Sign In"),\
       logging.error("Failed to Sign In")

       assert spice.sign_in_app.verify.on_page(),\
       logging.error("Not on Sign In page")

       assert spice.sign_in_app.printer_user.select_method(),\
       logging.error("Failed to select Printer User sign in method")

       assert spice.sign_in_app.printer_user.enter_username(user_name),\
       logging.error(f"Failed to enter username: {user_name}")

       assert spice.sign_in_app.printer_user.enter_password(password),\
       logging.error(f"Failed to enter password: {password}")

       assert spice.sign_in_app.printer_user.click_sign_in_button(),\
       logging.error("Failed to click sign in button")

       assert spice.sign_in_app.verify.welcome_user_toast_message(user_name),\
       logging.error("Failed to find Welcome User toast message")
    
       assert spice.universal_sign_in_app.is_signed_in(),\
       logging.error("Failed to Sign In")

       copy_job_app = spice.copy_ui()
       copyApp = copy_job_app.get_copy_app()
       copyApp.mouse_click()
       copy_job_app.click_home_button()
    except Exception as exception:
       assert False, f"Exception caught: {exception}"
    finally:
        spice.signIn.goto_universal_sign_in("Sign Out")
        cdm.device_user.delete_user(user_name)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test the CopyColor RBAC permissions in the CopyApp with print user allowed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-78676
    +timeout:1000
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_color_ui_permissions_printerUserAllowed_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_color_ui_permissions_printerUserAllowed_subject
        +guid:c6ec6b8f-63b4-43ff-8afa-8a7523cd9d1b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & Authentication=Sign-in & DeviceFunction=CopyColor & Copy=GrayScale & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_color_ui_permissions_printerUserAllowed_subject(spice,cdm,udw,job,ews,net):
    try:
        cdm.device_user.create_user('tester', '', 'Test@13579', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)

        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopyColor,DEVICEUSER_ROLE_USER,True)

        logging.info("Step 1: Enter valid credentials")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        try:
            spice.status_center.collapse()
        except:
            pass
        # Go to Copy options
        copy_job_app = spice.copy_ui()
        copyApp = copy_job_app.get_copy_app()
        copyApp.mouse_click()
        time.sleep(5)

        # Verify if Color is selected in ColorMode
        copy_job_app.goto_copy_options_list()
        copy_job_app.goto_copy_option_color_screen()
        copy_job_app.check_spec_on_copy_options_color(net, "all")
        spice.copy_ui().back_to_landing_view()

    finally:
        spice.copy_ui().goto_menu_mainMenu()
        spice.signIn.goto_universal_sign_in("Sign Out")
        cdm.device_user.deleteallusers()
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopyColor,GuestRoleGuid,True)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the QuickCopyJob RBAC permissions with print user allowed
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-179543
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickCopy_footer_permissions_printerUserAllowed_subject
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:PermissionUserRoles
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickCopy_footer_permissions_printerUserAllowed_subject
        +guid:9bef30d8-1d85-11ef-833f-0fca627ac8ac
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Footer 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
""" 
def test_copy_ui_quickCopy_footer_permissions_printerUserAllowed_subject(spice,cdm,udw,job,ews,net):
    try:
        cdm.device_user.create_user('tester', '', 'Test@13579', 'displayname1', 'user1@email.com', 'networkuser1', DEVICEUSER_ROLE_USER)

        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopy,DEVICEUSER_ROLE_USER,True)

        logging.info("Step 1: Enter valid credentials")

        spice.signIn.goto_universal_sign_in("Sign In")
        spice.signIn.select_device_user_login()
        spice.signIn.enter_creds(login=True,authAgent="user", password="Test@13579", username="tester")

        assert spice.signIn.verify_auth("success"), "Login with valid device user credentials failed"
        
        # Go to CopyApp
        copy_job_app = spice.copy_ui()
        #extend the test case to be run on widget also
        copyApp = copy_job_app.perform_copy_from_homescreen_footer()
        time.sleep(5)

        #time.sleep(3)
        #spice.goto_homescreen()

        spice.signIn.verifyPermissionEnforced(expected = True)
        #spice.signIn.cleanup("user", "success")

    finally:
        spice.copy_ui().goto_menu_mainMenu()
        spice.signIn.goto_universal_sign_in("Sign Out")
        cdm.device_user.deleteallusers()
        ews.security_app.access_control_page.permissions_tab.set_permission_ews(PermissionCopyColor,GuestRoleGuid,True)
