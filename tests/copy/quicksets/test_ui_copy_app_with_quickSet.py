import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.send.common import common
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy

def verify_copy_default_ticket_quality(cdm, changedValue):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert changedValue == ticket_default_body["dest"]["print"]["printQuality"]

def verify_copy_default_ticket_color(cdm, changedValue):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert changedValue == ticket_default_body["src"]["scan"]["colorMode"]

def verify_copy_default_content_type(cdm, changedValue):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert changedValue == ticket_default_body["src"]["scan"]["contentType"]

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:If no quickset is selected default quickset should be selected
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui__validate_default_quickset_function_from_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui__validate_default_quickset_function_from_landingapp
        +guid:3429f88a-6f36-416d-abfb-a972a4f4244d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui__validate_default_quickset_function_from_landingapp(job, udw, spice, net, cdm, configuration):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    adfLoaded = True
    common_instance = common.Common(cdm, udw)
    loadmedia = common_instance.scan_resource()
    loadmedia = "Flatbed" if loadmedia == "Glass" else loadmedia

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)
        if loadmedia == "Flatbed":
            adfLoaded = False
        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().start_copy(familyname = configuration.familyname, adfLoaded=adfLoaded)
        if job.job_concurrency_supported == "false":
            spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Change the option in default quickset and save it and call the action
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_from_default_quickset_modification_from_options_save_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_from_default_quickset_modification_from_options_save_landingapp
        +guid:edb9818b-71f9-4e7a-942b-511b5f08434e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_from_default_quickset_modification_from_options_save_landingapp(job, net, udw, spice, cdm):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    
    support_sign_in_app_from_fp = spice.signIn.support_sign_in_app_from_fp()

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        time.sleep(2)
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_options_list()
        if cdm.device_feature_cdm.is_color_supported():
            spice.copy_ui().select_color_mode("Grayscale")
        else:
            spice.copy_ui().select_content_type("Text")

        # spice.copy_ui().select_color_mode("Grayscale")
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()
        time.sleep(3)

        if cdm.device_feature_cdm.is_color_supported():
            verify_copy_default_ticket_color(cdm, 'grayscale')
        else:
            verify_copy_default_content_type(cdm, 'text')

        spice.copy_ui().start_copy()
        time.sleep(10)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
        # wait for copy toast message dismiss
        time.sleep(10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        if support_sign_in_app_from_fp:
            spice.signIn.goto_universal_sign_in("Sign Out")

        Copy.reset_copy_default_ticket(cdm, ticket_default_body)
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:select a quickset from quickset list and perform the opration
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_non_default_quickset_function_from_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_non_default_quickset_function_from_landingapp
        +guid:9c95399b-43e5-4574-873c-29eccc9f947e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_validate_non_default_quickset_function_from_landingapp(cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)
        spice.copy_ui().start_copy()
        if job.job_concurrency_supported == "false":
            spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Entry Exit of Copy App quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-125635
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_walkupapp_copy_ui_extry_exit_with_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_walkupapp_copy_ui_extry_exit_with_quickset
        +guid:0f6a6d95-a921-493f-bf75-a615576c3b01
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & DeviceFunction=Quickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_walkupapp_copy_ui_extry_exit_with_quickset(cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT  + "/" + jobticket_id
        shortcut_id1 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id1, "scan", [
                                   "print"], "open", "true", False, href)
        time.sleep(3)
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT  + "/" + jobticket_id
        shortcut_id2 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("anotherQuickset", shortcut_id2, "scan", [
                                   "print"], "open", "true", False, href)

        spice.copy_ui().goto_copy()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id1)
        csc.delete_shortcut(shortcut_id2)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:select a quickset from quickset list and re-select same quickset, validate same quickset settings are applied
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-125635
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_selection_of_quickset_via_viewall
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_selection_of_quickset_via_viewall
        +guid:416120b4-d629-415e-b8b2-4396fa307ab5
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_selection_of_quickset_via_viewall(cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        if cdm.device_feature_cdm.is_color_supported():      
            color_mode = 'color'
        else:
            color_mode = 'grayscale'
        custom_copy_configuration_payload =  {
            "src": {
                    "scan": {
                    "colorMode": color_mode
                    }
                },
            "dest": {
                "print": {
                    "copies": 2,
                }
            }
        }
        response = cdm.patch_raw(href, custom_copy_configuration_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL"
        shortcut_id1 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id1, "scan", [
                                   "print"], "open", "true", False, href)
        time.sleep(3)
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        custom_copy_configuration_payload =  {
            "src": {
                    "scan": {
                    "colorMode": color_mode
                    }
                },
            "dest": {
                "print": {
                    "copies": 4,
                }
            }
        }
        response = cdm.patch_raw(href, custom_copy_configuration_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL"
        shortcut_id2 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("anotherQuickset", shortcut_id2, "scan", [
                                   "print"], "open", "true", False, href)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        time.sleep(10)
        spice.copy_ui().select_copy_quickset("#"+shortcut_id1)

        spice.copy_ui().verify_selected_quickset(shortcut_id1)

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id1)
        csc.delete_shortcut(shortcut_id2)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test save option for selected quickset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_from_non_default_quickset_modification_from_options_save_landingapp
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_from_non_default_quickset_modification_from_options_save_landingapp
        +guid:dcb918cd-ab8e-482d-b140-3af88685fd16
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=GrayScale & Quicksets=DefaultQuickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_from_non_default_quickset_modification_from_options_save_landingapp(cdm, job, spice, net, udw):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    support_sign_in_app_from_fp = spice.signIn.support_sign_in_app_from_fp()
    try:
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy2", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)
        spice.copy_ui().goto_copy_options_list()
        if cdm.device_feature_cdm.is_color_supported(): 
            spice.copy_ui().select_color_mode("Grayscale")
        else:
            spice.copy_ui().select_content_type("Text")
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()
        time.sleep(3)

        if cdm.device_feature_cdm.is_color_supported():
            verify_copy_default_ticket_color(cdm, 'grayscale')
        else:
            verify_copy_default_content_type(cdm, 'text')
            
        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        if support_sign_in_app_from_fp:
            spice.signIn.goto_universal_sign_in("Sign Out")

        Copy.reset_copy_default_ticket(cdm, ticket_default_body)

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Validate quickset with same name
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_quickset_with_samename
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_quickset_with_samename
        +guid:f450c094-d3cf-4e6b-a52e-91cdbae804fb
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=IDCopy & Quicksets=DefaultQuickset
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_validate_quickset_with_samename(cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        shortcut_id1 = str(uuid.uuid4())
        shortcut_id2 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopySameName", shortcut_id1,
                                   "scan", ["print"], "open", "true", False, csc.JobTicketType.COPY)
        csc.create_custom_shortcut("MyCopySameName", shortcut_id2,
                                   "scan", ["print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id1)
        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id1)
        csc.delete_shortcut(shortcut_id2)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Create Copy Quickset, Delete Copy Quickset and validate
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-28633
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_create_quickset_then_delete_validate
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_create_quickset_then_delete_validate
        +guid:9afef67b-5ce1-492e-b0c3-01ad7a4882be
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_create_quickset_then_delete_validate(cdm, spice, net):

    try:

        csc = CDMShortcuts(cdm, net)
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        shortcut_id1 = str(uuid.uuid4())
        csc.create_custom_shortcut("MyCopyDeleteLater", shortcut_id1,
                                   "scan", ["print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        time.sleep(2)
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id1)
        spice.copy_ui().goto_copy_quickset_view()

        spice.copy_ui().select_copy_quickset("#Default")
        csc.delete_shortcut(shortcut_id1)
        # spice.copy_ui().goto_copy_quickset_view()
        try:
            spice.query_item("#MyCopyDeleteLater") == None
            assert False
        except Exception:
            assert True

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:select a quickset from quickset list and re-select default quickset, validate default quickset settings are applied
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-97714
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_default_quickset_settings_applied_after_selecting_factory_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_validate_default_quickset_settings_applied_after_selecting_factory_quickset
        +guid:6a461ca1-99e1-49d7-9de9-41d8a56b6fdd
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=Quality & Quicksets=DefaultQuickset
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name


def test_copy_ui_validate_default_quickset_settings_applied_after_selecting_factory_quickset(cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        custom_copy_configuration_payload =  {
            "dest": {
                "print": {
                    "copies": 2,
                    "printQuality": "best"
                }
            }
        }
        response = cdm.patch_raw(href, custom_copy_configuration_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL"
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, href)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)

        # verify that setting of selected quickset has been applied
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "quality", "best")
        spice.copy_ui().back_to_landing_view()
        # Now Again Select the default quickset and verify it properties, is set to default
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#Default")
        # verify that setting of selected quickset has been applied
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "quality", "standard")
        spice.copy_ui().back_to_landing_view()

        spice.copy_ui().start_copy()
        if job.job_concurrency_supported == "false":
            spice.copy_ui().wait_for_release_page_prompt_and_click_relasePage()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test save option for auto color mode selected quickset
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_quickset_modification_from_options_color_landing
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_quickset_modification_from_options_color_landing
        +guid:71eaea3d-1c84-41ee-a25c-20c22270b33d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_quickset_modification_from_options_color_landing(cdm, job, spice, net, udw):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    try:
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy1", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        
        verify_copy_default_ticket_color(cdm, 'autoDetect')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)
        spice.copy_ui().select_color_mode_landing(option="Color")
        spice.copy_ui().save_as_default_copy_ticket()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#Default")
        
        verify_copy_default_ticket_color(cdm, 'color')
        spice.copy_ui().select_color_mode_landing(option="Automatic")
        spice.copy_ui().save_as_default_copy_ticket()
        
        verify_copy_default_ticket_color(cdm, 'autoDetect')

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        spice.signIn.goto_universal_sign_in("Sign Out")
        Copy.reset_copy_default_ticket(cdm, ticket_default_body)
        # delete previously added shorcut
        csc.delete_all_shortcuts()       

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:select a quickset from quickset list and re-select default quickset, validate default quickset settings are applied
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_validate_default_quickset_colormode_autodetect
    +test:
        +title:test_copy_ui_validate_default_quickset_colormode_autodetect
        +guid:e269c40e-3257-43aa-8985-3e002378aebb
        +dut:
            +type:Simulator
            +configuration:Copy=Color & ScanColorMode=Automatic
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_validate_default_quickset_colormode_autodetect(scan_emulation, cdm, udw, spice, net, job):
    scan_emulation.media.load_media(media_id='ADF')
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        custom_copy_configuration_payload =  {
            "src": {
                    "scan": {
                    "colorMode": "color"
                    }
                },
            "dest": {
                "print": {
                    "copies": 2,
                }
            }
        }
        response = cdm.patch_raw(href, custom_copy_configuration_payload)
        assert response.status_code == 200, "PATCH OPERATION WAS SUCCESSFUL"
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id, "scan", [
                                   "print"], "open", "true", False, href)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#"+shortcut_id)

        # verify that setting of selected quickset has been applied
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "color", "color")
        spice.copy_ui().back_to_landing_view()
        # Now Again Select the default quickset and verify it properties, is set to default
        spice.copy_ui().goto_copy_quickset_view()
        spice.copy_ui().select_copy_quickset("#Default")
        # verify that setting of selected quickset has been applied
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().verify_copy_settings_selected_option(net, "color", "automatic")
        spice.copy_ui().back_to_landing_view()

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)
