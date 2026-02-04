"""
Name: UiPermissionsTestHelper.py
Author: Joshua Byers
Date: 5/27/2022
"""
import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.SignInAppWorkflowObjectsIds import SignInAppWorkflowObjectIds
from tests.security.accountManagement.WindowsAuth.WindowsAuthTestHelper import WindowsAuthTestHelper
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUICommonOperations import WorkflowUICommonOperations

# Declare the auth agents
AGENT_WINDOWS = "5470b2ae-29cf-415b-a22d-349b50c9cb13"
AGENT_LDAP = "8a3a1a8c-773f-8b17-1dc6-1780745631a2"

# Declare the role UUIDs
ROLE_GUEST = "0a52b510-5db2-49f2-b95d-7f5c37c50235"
ROLE_DEVICE_USER = "a69a546c-dd68-4e4b-8302-97cd6471a0a4"
ROLE_ADMIN = "42e5e2d7-6c01-42b8-b086-ee8a1a2c25de"
ROLE_SERVICE = "b3f47689-7387-4f67-90e3-17bea2ba7137"
ROLE_WINDOWS = "WINDOWS"
ROLE_LDAP = "LDAP"

def signInByRole(spice, signInMethod, defaultAuthAgent, enterSignInApp):
    """
    Method to completely sign into a role. Provides UI navigation and credentials.

    Inputs:
        signInMethod: Role to log into (OPTIONS: "user", "admin", "windows", "ldap")
        defaultAuthAgent: Default auth agent for system or permission
        enterSignInApp: If True, Sign In app will be selected from the home screen

    Returns:
        True if sign in was successful
    """
    # If the default auth agent is the desired auth agent, there is no need to reselect the method
    if enterSignInApp:
        spice.signIn.goto_universal_sign_in("Sign In") #Home screen click to app

    if signInMethod != defaultAuthAgent:
        spice.signIn.select_sign_in_method(signInMethod, defaultAuthAgent)

    if signInMethod == "user":
        logging.info("Logging in as Printer User")
        spice.signIn.enter_creds(True, signInMethod, "Pass12345", "Printer User")

    elif signInMethod == "admin":
        logging.info("Logging in as Device Admin")
        spice.signIn.enter_creds(True, signInMethod, "12345678")

    elif signInMethod == "windows":
        logging.info("Logging in as Windows")
        userinfo = WindowsAuthTestHelper.get_user('keymaster')
        spice.signIn.enter_creds(True, signInMethod, userinfo['Password'], userinfo['SamAccountName'])

    elif signInMethod == "ldap":
        logging.info("Logging in as LDAP")
        spice.signIn.enter_creds(True, signInMethod, "xyzzy_123", "keymaster")

    response = spice.signIn.verify_auth("success")
    return response


def sign_in_test_sign_out(spice, permission:str, role:str, defaultAuth:str, permissionGranted:bool):
    """
    Method signs into role, navigates to the test permission,
    confirms permission granted/denied, returns home, and signs out.

    Inputs:
        cdm: cdm object
        spice: spice object
        permission: GUID of permission being tested
        role: Name of role being tested (OPTIONS: "user", "admin", "windows", "ldap")
        defaultAuth: Name of default role expected on sign in screen (OPTIONS: "user", "admin", "windows", "ldap")
        permissionGranted: True if expected access granted, False if expecting access denied

    Returns:
        True if permission is granted/denied as expected
    """
    # Sign in and verify default auth agent
    result = signInByRole(spice, role, defaultAuth, True)
    # Verify sign in was successful
    if result == False:
        return result
    time.sleep(5)
    # Navigate to the permission
    spice.signIn.goto_permission(permission)
    time.sleep(3)
    # Confirm permission access enforced
    result = spice.signIn.verifyPermissionEnforced(permissionGranted)
    # Return to the home screen
    if permissionGranted:
        # Return home from permission page
        spice.signIn.goto_home_from_permission(permission, True)
    else:
        # Return home from permission button (one page before permission)
        spice.signIn.goto_home_from_permission(permission, False)
    # Sign out
    spice.signIn.cleanup(role, "success")
    # Return after signing out
    return result

def lazy_auth_test_sign_out(spice, permission:str, role:str, defaultAuth:str, permissionGranted:bool):
    """
    Method navigates to the test permission as guest, signs into role,
    confirms permission granted/denied, returns home, and signs out.

    Inputs:
        cdm: cdm object
        spice: spice object
        permission: GUID of permission being tested
        role: Name of role being tested (OPTIONS: "user", "admin", "windows", "ldap")
        defaultAuth: Name of default role expected on sign in screen (OPTIONS: "user", "admin", "windows", "ldap")
        permissionGranted: True if expected access granted, False if expecting access denied

    Returns:
        True if permission is granted/denied as expected
    """
    # Navigate to the permission
    spice.signIn.goto_permission(permission)
    # Sign in as Device User and verify custom default agent is set (LDAP)
    result = signInByRole(spice, role, defaultAuth, False)
    # Verify sign in was successful
    if result == False:
        return result
    time.sleep(5)
    # Confirm permission access granted
    result = spice.signIn.verifyPermissionEnforced(permissionGranted)
    time.sleep(3)
    # Return to the home screen
    if permissionGranted:
        # Return home from permission page
        spice.signIn.goto_home_from_permission(permission, True)
    else:
        # Return home from permission button (one page before permission)
        spice.signIn.goto_home_from_permission(permission, False)
    # Sign out
    spice.signIn.cleanup(role, "success")
    # Return after signing out
    return result

def permission_test_procedure(cdm, spice, uuid):

    logging.debug(f"testPermission: {uuid}")

    # Set auth agent for the permission (LDAP)
    assert cdm.rbac.set_permission_auth_agent(uuid, AGENT_LDAP),\
        "Test failed (Unable to set default auth agent for permission)"

    # Reload the permissions on the UI by signing in and signing out
    signInByRole(spice, "admin", "windows", True)
    spice.signIn.cleanup("admin", "success")

    # Navigate to permission as Guest
    spice.signIn.goto_permission(uuid)
    # Verify default agent for the permission by changing sign in method
    spice.signIn.select_sign_in_method("admin", "ldap")
    # Return to home screen
    result = spice.signIn.go_home_from_sign_in()
    spice.goto_homescreen()
    assert result, "Test failed (Could not return to home screen after verifying system default auth agent)"

    # --------------------------------------
    #           Standard Sign In
    # --------------------------------------
    result = sign_in_test_sign_out(spice, uuid, "windows", "windows", False)
    assert result, "Test failed (Permission granted, expected denied)"

    result = sign_in_test_sign_out(spice, uuid, "user", "windows", True)
    assert result, "Test failed (Permission denied, expected granted)"

    result = sign_in_test_sign_out(spice, uuid, "admin", "windows", True)
    assert result, "Test failed (Permission denied, expected granted)"

    result = sign_in_test_sign_out(spice, uuid, "ldap", "windows", True)
    assert result, "Test failed (Permission denied, expected granted)"

    # --------------------------------------
    #               Lazy Auth
    # --------------------------------------
    result = lazy_auth_test_sign_out(spice, uuid, "windows", "ldap", False)
    assert result, "Test failed (Permission granted, expected denied)"

    result = lazy_auth_test_sign_out(spice, uuid, "user", "ldap", True)
    assert result, "Test failed (Permission denied, expected granted)"

    result = lazy_auth_test_sign_out(spice, uuid, "admin", "ldap", True)
    assert result, "Test failed (Permission denied, expected granted)"

    result = lazy_auth_test_sign_out(spice, uuid, "ldap", "ldap", True)
    assert result, "Test failed (Permission denied, expected granted)"
