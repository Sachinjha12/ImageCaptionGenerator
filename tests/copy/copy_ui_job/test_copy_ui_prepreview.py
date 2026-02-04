import logging
from dunetuf.copy.copy import *
import json
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To Check prepreview panel content in mdf
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-91628
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_ui_verify_prepreview_screen_mdf
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_verify_prepreview_screen_mdf
        +guid:9847af6c-ad2f-4ec4-9466-068483aa25ed
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder & Copy=ImagePreview
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_verify_prepreview_screen_mdf(spice, job, cdm, udw, net):
    try:
        job.bookmark_jobs()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        copy_job_app.verify_prepreview_screen_string_mdf(udw,net)
        copy_job_app.goto_main_panel()
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To verify page modifications are being retained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-83903
    +timeout:300
    +asset:Copy
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +feature_team:CopySolns
    +delivery_team:WalkupApps
    +name:test_copy_ui_inspect_page_modifications
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_inspect_page_modifications
        +guid:42ac77f5-a70e-4635-8d50-4e6dc2ad37ff
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & EngineFirmwareFamily=DoX & DeviceFunction=Copy & ScannerInput=ManualFeeder & Copy=ImagePreview & Copy=ImageEdition
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_inspect_page_modifications(spice, job, cdm, udw, net):
    try:
        job.bookmark_jobs()
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_preview_panel()
        udw.mainApp.ScanMedia.loadMedia("MDF")
        copy_job_app.start_copy()
        #JobTicketResourceManager PUB_getAllJobTicketIDs
        command_output = udw.mainApp.JobTicketResourceManager.getAllJobTicketIDs()
        ids = command_output.split('\n')
        last_job_id = ids[len(ids)-1]
        print(f"test_copy_ui_inspect_page_modifications: last_job_id {last_job_id}")
        pages_url = cdm.JOB_TICKET_MODIFY_ENDPOINT.format(last_job_id) + "/pages"
        print(f"pages_url: {pages_url}")
        pages = cdm.get(pages_url)
        pageTickets = pages['pageTickets']
        
        #print("pages:")
        #print(pageTickets)
        my_page_ticket_url = pageTickets[0]['links'][1]['href']
        print("page ticket url:")
        print(my_page_ticket_url)
        my_page_ticket = cdm.get(my_page_ticket_url)
        #print("my_page_ticket:")
        #print(my_page_ticket)
        my_page_ticket['modifications']['brightness'] = 4
        my_page_ticket['modifications']['highlight'] = 5
        cdm.patch(my_page_ticket_url, my_page_ticket)
        my_page_ticket = cdm.get(my_page_ticket_url)

        #print("Page Ticket:")
        #print(my_page_ticket)
        assert my_page_ticket['modifications']['brightness'] == 4
        assert my_page_ticket['modifications']['highlight']  == 5

    finally:
        job.cancel_active_jobs()
        spice.goto_homescreen()
        pass
