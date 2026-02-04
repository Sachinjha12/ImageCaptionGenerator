import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy

def verify_copy_default_ticket_quality(cdm, changedValue):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert changedValue == ticket_default_body["dest"]["print"]["printQuality"]

def verify_copy_default_ticket_color(cdm, changedValue):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert changedValue == ticket_default_body["src"]["scan"]["colorMode"]

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Entry Exit of Copy App quickset
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-125635
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_extry_exit_with_quickset
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_ui_extry_exit_with_quickset
        +guid:85cdf985-d9c8-48a9-ac98-be9a0cf9dec9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy  & EWS=Quicksets

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_extry_exit_with_quickset(setup_teardown_with_copy_job, cdm, udw, spice, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        shortcut_id1 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("MyCopy", shortcut_id1, "scan", [
                                   "print"], "open", "true", False, href)
        time.sleep(3)
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
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
    +purpose: Checking the order of Quicksets
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-191742
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_with_quickset_check_sorting_order
    +categorization:
        +segment:Platform
        +area:QuickSet
        +feature:Copy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_with_quickset_check_sorting_order
        +guid:67516edf-f1e2-4c5a-aba7-d16c75b600ae
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_with_quickset_check_sorting_order(cdm, udw, net, job):

    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    csc = CDMShortcuts(cdm, net)
    existing_shortcuts = csc.get_all_shortcuts()
    if existing_shortcuts:
        deleteshortcuts = csc.delete_all_shortcuts()
    try:
        shortcut_titles = []
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        shortcut_id1 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("1", shortcut_id1, "scan", [
                                   "print"], "open", "true", False, href)
        
        time.sleep(3)
        shortcut_titles.append("1")
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        shortcut_id2 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("2", shortcut_id2, "scan", [
                                   "print"], "open", "true", False, href)

        time.sleep(3)
        shortcut_titles.append("2")
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id
        shortcut_id3 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("3", shortcut_id3, "scan", [
                                   "print"], "open", "true", False, href)

        time.sleep(3)
        shortcut_titles.append("3")
        csc = CDMShortcuts(cdm, net)
        jobticket_id = csc.create_jobticket(csc.JobTicketType.COPY)
        # Create quickset
        href = cdm.JOB_TICKET_ENDPOINT + "/" + jobticket_id

        shortcut_id4 = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut_with_href("4", shortcut_id4, "scan", [
                                   "print"], "open", "true", False, href)
        shortcut_titles.append("4")
        shortcuts = csc.get_all_shortcuts()

        for i in range(0, len(shortcuts)):
            assert shortcuts[i]["title"] == shortcut_titles[i]
    
    finally:
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id1)
        csc.delete_shortcut(shortcut_id2)
        csc.delete_shortcut(shortcut_id3)
        csc.delete_shortcut(shortcut_id4)