import logging
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import *
import json
import pprint
import logging

from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds


def verify_copy_default_ticket(cdm):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    # assert 'draft' == ticket_default_body["dest"]["print"]["printQuality"]
    assert 'photo' == ticket_default_body["src"]["scan"]["contentType"]
    assert 'iso_a4_210x297mm' == ticket_default_body["src"]["scan"]["mediaSize"]
    assert 'twoUp' == ticket_default_body["pipelineOptions"]["imageModifications"]["pagesPerSheet"]
    assert 'grayscale' == ticket_default_body["src"]["scan"]["colorMode"]

def verify_copy_default_ticket_2(cdm):
    ticket_default_body = Copy.get_copy_default_ticket(cdm)
    assert 'duplex' == ticket_default_body["src"]["scan"]["plexMode"]
    assert 'tray-2' == ticket_default_body["dest"]["print"]["mediaSource"]
    #assert 'na_legal_8.5x14in' == ticket_default_body["dest"]["print"]["mediaSize"]
    assert 'stationery' == ticket_default_body["dest"]["print"]["mediaType"]
    assert 8 == ticket_default_body["pipelineOptions"]["imageModifications"]["exposure"]
    assert 'uncollated' == ticket_default_body["dest"]["print"]["collate"]
    assert 'true' == ticket_default_body["src"]["scan"]["pagesFlipUpEnabled"]
    
def source_destination(source,dest):
    return {'src': {source:{}}, 'dest': {dest:{}} }

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 2up adf and verify output scale is constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-95017
    +timeout:420
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_2up_verify_output_scale_constrained
    +test:
        +title:test_copy_ui_2up_verify_output_scale_constrained
        +guid:96bcff8f-91d4-4fea-b9db-63f9e30cf462
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2up_verify_output_scale_constrained(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()

    logging.info("Load ADF")
    scan_emulation.media.load_media('ADF',2)

    logging.info("Go to Copy > Options, set Pages per sheet to 2")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.select_pages_per_sheet_option(udw, option='2')

    logging.info("Verify that output scale is disabled")
    copy_job_app.verify_copy_option_output_scale_constrained(configuration)

    logging.info("Go back Copy Landing screen")
    copy_job_app.back_to_landing_view()

    logging.info("Start a copy job")
    copy_job_app.start_copy()

    logging.info("Validate copy settings for current job")
    Copy(cdm, udw).validate_settings_used_in_copy(pages_per_sheet='twoUp', media_source='adf')

    logging.info("Check the copy job complete successfully")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    logging.info("Back to the home screen")
    spice.goto_homescreen()


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with Fit to Page setting and verify that pages per sheet option is constrained
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-95017
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_output_scale_option_verify_nup_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_output_scale_option_verify_nup_constrained
        +guid:277b3cda-b9f4-44fb-83a4-3e4040ddca1b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=ResizeCustom & Copy=2PagesPerSheet 
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_output_scale_option_verify_nup_constrained(scan_emulation, setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration):
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set collate on")
    copy_job_app.change_collate(collate_option="on")
    logging.info("set the fit to page to output scale")
    copy_job_app.select_resize_option("Custom")

    logging.info("Verify that page per sheet option is constrained")
    copy_job_app.verify_copy_pages_per_sheet_constrained(udw, net)
    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    scaleToFitEnabled = 'false'
    if configuration.familyname == 'enterprise':
        scaleToFitEnabled = 'true'
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        sides="oneSided",
        orientation="portrait",
        content_type="mixed",
        two_side_page_flip_up="false",
        pages_per_sheet="oneUp",
        collate="collated",
        output_scale_setting = {'scaleToFitEnabled': scaleToFitEnabled, 'xScalePercent': 100, 'yScalePercent': 100, 'scaleSelection': 'custom'})
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])



'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy with flatbed loaded and verify that collate option is constrained
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-96412
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_flatbed_verify_collate_constraint
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_flatbed_verify_collate_constraint
        +guid:89f3f7ac-9e03-4a35-b0a3-b6c16a14a027
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=Quality & Copy=Collation & ImagePreview=Refresh
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_ui_flatbed_verify_collate_constraint(setup_teardown_with_copy_job, job, spice, net, cdm, udw, configuration):
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Load ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("Verify that collate option is constrained")
    copy_job_app.verify_copy_collate_constrained()
    logging.info("change other option")
    copy_job_app.select_content_type("Photograph")
    logging.info("Verify that collate option is still constrained")
    copy_job_app.verify_copy_collate_constrained()
    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    logging.info("wait until copying complete")
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    udw.mainApp.ScanMedia.loadMedia("ADF")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test pagespersheet constraints on original size Mixed settings for copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106570
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_originalSize_mixed_option_verify_nup_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_originalSize_mixed_option_verify_nup_constrained
        +guid:06692d8e-3313-4c74-922e-f3937c5e3dd9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A3 & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_originalSize_mixed_option_verify_nup_constrained(scan_emulation, job, spice, net, cdm, udw, configuration, tray):
    try:
        scan_emulation.media.load_media(media_id='ADF')
        udw.mainApp.ScanDeviceService.setNumScanPages(4)

        logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
        job.bookmark_jobs()
        logging.info("Go to copy screen")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        logging.info("set original size to Mixed")
        copy_job_app.select_original_size("MIXED_LETTER_LEDGER")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_pages_per_sheet_constrained(udw, net)
        copy_job_app.select_original_size("MIXED_LETTER_LEGAL")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_pages_per_sheet_constrained(udw, net)
        copy_job_app.select_original_size("MIXED_A4_A3")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_pages_per_sheet_constrained(udw, net)

        logging.info("Back to copy screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start to copy")
        copy_job_app.start_copy(dial_value=0)
        Copy(cdm, udw).validate_settings_used_in_copy(
            number_of_copies=1,
            tray_setting="auto",
            original_size="com.hp.ext.mediaSize.mixed-a4-a3",
            orientation="portrait",
            content_type="mixed",
            pages_per_sheet="oneUp")
        logging.info("wait until copying complete")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        logging.info("check the job state from cdm")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        logging.info("back to the home screen")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test paper sources constraints on original size Mixed settings for copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106570
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_originalSize_mixed_option_verify_paper_sources_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_originalSize_mixed_option_verify_paper_sources_constrained
        +guid:648ff07e-97e3-4632-9b50-bd21fa5a3f6e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy &  ADFMediaSize=A3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_originalSize_mixed_option_verify_paper_sources_constrained(scan_emulation, job, spice, net, cdm, udw, configuration):
    scan_emulation.media.load_media(media_id='ADF')
    logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
    job.bookmark_jobs()
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("go to options screen")
    copy_job_app.goto_copy_options_list()
    logging.info("set original size to Mixed")
    copy_job_app.select_original_size("MIXED_LETTER_LEDGER")
    logging.info("Verify that page per sheet option is constrained")
    copy_job_app.verify_copy_paper_source_constrained()
    copy_job_app.select_original_size("MIXED_LETTER_LEGAL")
    logging.info("Verify that page per sheet option is constrained")
    copy_job_app.verify_copy_paper_source_constrained()
    copy_job_app.select_original_size("MIXED_A4_A3")
    logging.info("Verify that page per sheet option is constrained")
    copy_job_app.verify_copy_paper_source_constrained()

    logging.info("Back to copy screen")
    copy_job_app.back_to_landing_view()
    logging.info("Start to copy")
    copy_job_app.start_copy(dial_value=0)
    Copy(cdm, udw).validate_settings_used_in_copy(
        number_of_copies=1,
        tray_setting="auto",
        original_size="com.hp.ext.mediaSize.mixed-a4-a3",
        orientation="portrait",
        content_type="mixed",
        pages_per_sheet="oneUp")
    logging.info("wait until copying complete")
    time.sleep(7)
    copy_job_app.media_mismatch_flow()
    copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
    logging.info("check the job state from cdm")
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    logging.info("back to the home screen")
    spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy 1-2 sided and 2-2 sided options disabled when unsupported mediasize is selecected and vice-versa
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-127473
    +timeout:600
    +asset:Copy
    +delivery_team:Home
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_sides_and_paperSize_constrained_apply_properly
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_sides_and_paperSize_constrained_apply_properly
        +guid:84328504-460e-40d1-9807-7459f9994e74
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Homesmb & ADFMediaSize=Legal
    +delivery_team:Home
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_sides_and_paperSize_constrained_apply_properly(job, udw, spice, cdm, net):
    try:
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        copy_job_app.select_copy_side("1_2_sided")
        copy_job_app.go_to_paper_selection()
        copy_job_app.select_media_size_option_constrained("na_legal_8.5x14in")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.select_copy_side("1_1_sided")
        copy_job_app.go_to_paper_selection()
        copy_job_app.select_media_size_option("Legal")
        copy_job_app.go_back_to_setting_from_paper_selection()

        copy_job_app.check_copy_side_constrained(net, "1_2_sided")
        copy_job_app.check_copy_side_constrained(net, "2_2_sided")
        copy_job_app.back_to_landing_view()
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test that copy 2-1 and 2-2 sides options are disabled when an unsupported original media size is selected, i.e duplex scanning of legal is disallowed. 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-132341
    +timeout:600
    +asset:Copy
    +delivery_team:Home
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_sides_and_originalSize_constrained_apply_properly
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_sides_and_originalSize_constrained_apply_properly
        +guid:8e45b17a-c88c-4ec3-aa56-928c634755fe
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEngineType=Homesmb & ADFMediaSize=Legal & Copy=2Sided2To1 & Copy=2Sided2To2
    +delivery_team:Home
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_sides_and_originalSize_constrained_apply_properly(job, udw, spice, cdm, net):
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        copy_job_app = spice.copy_ui()
        copy_job_app.enable_duplex_supported(cdm,udw)
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        copy_job_app.select_original_size("Legal")

        copy_job_app.check_copy_side_constrained(net, "2_2_sided")
        copy_job_app.check_copy_side_constrained(net, "2_1_sided")
        copy_job_app.back_to_landing_view()
        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")
    finally:
        spice.goto_homescreen()
        spice.copy_ui().disable_duplex_supported(cdm,udw)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy PagePerSheet is set to twoup, Mixed Size Constraint of Original Size is activated
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106571
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_verify_mixed_originalSize_constrained_apply
    +test:
        +title:test_copy_ui_option_verify_mixed_originalSize_constrained_apply
        +guid:cac2b5ca-a74c-44ea-8be4-a76536f26f94
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLegal & Copy=ResizeCustom
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_verify_mixed_originalSize_constrained_apply(scan_emulation, job, udw, spice, cdm):
    try:
        scan_emulation.media.load_media(media_id='ADF')
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        copy_job_app.select_resize_option("Custom")
        copy_job_app.goto_copy_option_original_size_screen()
        time.sleep(3)
        copy_job_app.verify_original_size_option_constrained("MIXED_LETTER_LEGAL")

        copy_job_app.select_resize_option("None")
        time.sleep(3)
        copy_job_app.select_original_size("MIXED_LETTER_LEGAL")

        copy_job_app.back_to_landing_view()
    finally:
        spice.goto_homescreen() 

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test Copy Ui Vaildate Constraint Message in MediaSize Constraint
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-130315
    +timeout:260
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_paperSize_validate_constrained_message
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_paperSize_validate_constrained_message
        +guid:678de433-14b3-405c-aff6-e102ac68e56d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & MediaSizeSupported=AnyCustom
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_paperSize_validate_constrained_message(spice, cdm):
    
    print("1. creating a new ticket")
   
    body = source_destination("scan","print")
    ticket_user_response = cdm.post_raw(cdm.JOB_TICKET_ENDPOINT, body)
    assert ticket_user_response.status_code == 201
    ticket_user_body = ticket_user_response.json()

    uri_put = cdm.JOB_TICKET_ENDPOINT + '/' +ticket_user_body['ticketId'] + '/constraints'
    response = cdm.get_raw(uri_put)
    assert response.status_code == 200

    constraints = response.json()
    paper_size_option_list = []
    paper_size_object_name = ""

    for i in range(0, len(constraints["validators"])):
        each_option = constraints["validators"][i]
        if(each_option["propertyPointer"] == "dest/print/mediaSize"):
            paper_size_option_list = each_option["options"]
            break
    
    for i in range(0, len(paper_size_option_list)):
        each_option = paper_size_option_list[i]
        if "disabled" in each_option.keys():
            paper_size_object_name = each_option["seValue"]
            break
    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        if(paper_size_object_name != ""):
            spice.copy_ui().select_media_size_option_constrained(paper_size_object_name, "This option is unavailable.")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up adf and verify output scale is constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_4up_right_then_down_verify_output_scale_constrained
    +test:
        +title:test_copy_ui_4up_right_then_down_verify_output_scale_constrained
        +guid:750f6a0f-1535-49d1-8b7f-b891e149b309
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=FourRightThenDownPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_right_then_down_verify_output_scale_constrained(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF')

        logging.info("Go to Copy > Options, set Pages per sheet to 2")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')

        logging.info("Verify that output scale is disabled")
        copy_job_app.verify_copy_option_output_scale_constrained(configuration)

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(pages_per_sheet='fourUp', numberUp_presentation_direction="toRightToBottom")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for 4up adf and verify output scale is constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:300
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_4up_down_then_right_verify_output_scale_constrained
    +test:
        +title:test_copy_ui_4up_down_then_right_verify_output_scale_constrained
        +guid:d1a8824b-dc8c-4ed7-a26b-ac8ab2415e79
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=FourDownThenRightPagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_4up_down_then_right_verify_output_scale_constrained(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load ADF")
        scan_emulation.media.load_media('ADF')

        logging.info("Go to Copy > Options, set Pages per sheet to 4_downThenRight")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.select_pages_per_sheet_option(udw, option='4_downThenRight')

        logging.info("Verify that output scale is disabled")
        copy_job_app.verify_copy_option_output_scale_constrained(configuration)

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(pages_per_sheet='fourUp', numberUp_presentation_direction="toBottomToRight")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy PagePerSheet is set to fourup, Mixed Size Constraint of Original Size is activated
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_4up_verify_mixed_originalSize_constrained_apply
    +test:
        +title:test_copy_ui_option_4up_verify_mixed_originalSize_constrained_apply
        +guid:20d10190-aea4-4c28-82a8-7624e4df5b38
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLegal & Copy=FourRightThenDownPagesPerSheet

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_4up_verify_mixed_originalSize_constrained_apply(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        scan_emulation.media.load_media(media_id='ADF')
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set Pages per sheet to 4_rightThenDown and verify constrained")
        copy_job_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')
        copy_job_app.goto_copy_option_original_size_screen()
        time.sleep(3)
        copy_job_app.verify_original_size_option_constrained("MIXED_LETTER_LEGAL")

        logging.info("set Pages per sheet to 4_DownThenRight and verify constrained")
        copy_job_app.select_pages_per_sheet_option(udw, option='4_downThenRight')
        copy_job_app.goto_copy_option_original_size_screen()
        time.sleep(3)
        copy_job_app.verify_original_size_option_constrained("MIXED_LETTER_LEGAL")

        logging.info("set Pages per sheet to 1 and original size MIXED_LETTER_LEGAL")
        copy_job_app.select_pages_per_sheet_option(udw, option='1')
        copy_job_app.select_original_size("MIXED_LETTER_LEGAL")

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(pages_per_sheet='oneUp', original_size="com.hp.ext.mediaSize.mixed-letter-legal")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to check constraint of Darkness/Constrast/Background Cleanup options when Auto tone is on
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-191053
    +timeout:500
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_validation_constrained_by_auto_tone_option
    +test:
        +title:test_copy_ui_option_validation_constrained_by_auto_tone_option
        +guid:69d4cbed-4c87-4722-a36b-9fc00565a767
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutomaticTone

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_validation_constrained_by_auto_tone_option(spice):
    try:
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        
        logging.info("Go to Auto tone Option and set Off > Verify that the auto tone option is a constraint")
        copy_job_app.goto_auto_tone_option()
        copy_job_app.set_copy_settings_auto_tone(auto_tone = False)
        copy_job_app.verify_copy_auto_tone_slider_constrained(constrained = True)
        
        logging.info("Go to Auto tone Option and set On > Verify that the auto tone option is not constraint")
        copy_job_app.goto_auto_tone_option()
        copy_job_app.set_copy_settings_auto_tone(auto_tone = True)
        copy_job_app.verify_copy_auto_tone_slider_constrained(constrained = False)
        
        logging.info("Check constraints of image adjustment options due to activation of auto tone option")
        copy_job_app.verify_copy_image_adjustment_options_constrained("auto_tone")
        copy_job_app.back_to_landing_view()
    
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test to check constraint of Darkness/Constrast/Background Cleanup options when Auto paper color removal is on
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-191053
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_validation_constrained_by_auto_paper_color_removal_option
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_validation_constrained_by_auto_paper_color_removal_option
        +guid:39cb0fa6-3cec-42fd-8a03-d70ec9685591
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanSettings=AutoPaperColorRemoval

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_validation_constrained_by_auto_paper_color_removal_option(spice):
    try:
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        
        logging.info("Go to Auto paper color option and set Off > Verify that the auto paper color option is a constraint")
        copy_job_app.goto_auto_paper_color_removal_option()
        copy_job_app.set_copy_settings_auto_paper_color_removal(auto_paper_color_removal = False)
        copy_job_app.verify_copy_auto_paper_color_removal_slider_constrained(constrained = True)
        
        logging.info("Go to Auto paper color option and set On > Verify that the auto paper color option is not constraint")
        copy_job_app.goto_auto_paper_color_removal_option()
        copy_job_app.set_copy_settings_auto_paper_color_removal(auto_paper_color_removal = True)
        copy_job_app.verify_copy_auto_paper_color_removal_slider_constrained(constrained = False)
        
        logging.info("Check constraints of image adjustment options due to activation of auto paper color option")
        copy_job_app.verify_copy_image_adjustment_options_constrained("auto_paper_color_removal")
        copy_job_app.back_to_landing_view()
    
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy PagePerSheet is set to fourup, Mixed Size Constraint of Original Size is activated
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-106812
    +timeout:800
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_verify_add_page_borders_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_verify_add_page_borders_constrained
        +guid:68384d1a-9fce-4201-af8a-8e7186178f3b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=AddPageBordersPagesPerSheet

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_verify_add_page_borders_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        scan_emulation.media.load_media(media_id='ADF')
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.verify_copy_add_page_borders_constrained(udw)

        logging.info("set Pages per sheet to 4_rightThenDown and verify constrained")
        copy_job_app.select_pages_per_sheet_option(udw, option='4_rightThenDown')
        copy_job_app.verify_copy_add_page_borders_constrained(udw, False)

        logging.info("set Pages per sheet to 4_DownThenRight and verify constrained")
        copy_job_app.select_pages_per_sheet_option(udw, option='4_downThenRight')
        copy_job_app.verify_copy_add_page_borders_constrained(udw, False)

        logging.info("set Pages per sheet to 1 and verify constrained")
        copy_job_app.select_pages_per_sheet_option(udw, option='1')
        copy_job_app.verify_copy_add_page_borders_constrained(udw, True)

        logging.info("set add page borders to True")
        copy_job_app.select_pages_per_sheet_option(udw, option='2')
        copy_job_app.select_add_page_borders_option(udw)

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(pages_per_sheet='twoUp', image_border='defaultLineBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy booklet format is set to on, borders on each page is not constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_verify_booklet_borders_on_each_page_constrained
    +test:
        +title:test_copy_ui_option_verify_booklet_borders_on_each_page_constrained
        +guid:533ddc2c-5a8c-48e2-b4b5-34d4bf37697f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_verify_booklet_borders_on_each_page_constrained(scan_emulation, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("set default options and verify borders on each page constrained")
        copy_job_app.verify_copy_booklet_borders_on_each_page_constrained(True)
        
        logging.info("Set booklet format to on.")
        copy_job_app.select_booklet_option('bookletFormat')

        logging.info("set booklet format and verify borders on each page constrained")
        copy_job_app.verify_copy_booklet_borders_on_each_page_constrained(False)

        logging.info("Set borders on each page to on.")
        copy_job_app.select_booklet_option('bordersOnEachPage')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy( 
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex",
            image_border='defaultLineBorder')

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:check copy from ui for booklet format and verify output scale is constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:360
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_booklet_format_verify_output_scale_constrained
    +test:
        +title:test_copy_ui_booklet_format_verify_output_scale_constrained
        +guid:5c918506-a67e-45d5-8525-3d5d4992cfe6
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_format_verify_output_scale_constrained(scan_emulation, spice, job, cdm, udw, net, configuration):
    job.bookmark_jobs()
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)

        logging.info("Go to Copy > Options, set Pages per sheet to 2")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("Set booklet format on")
        copy_job_app.select_booklet_option('bookletFormat')

        logging.info("Verify that output scale is disabled")
        copy_job_app.verify_copy_option_output_scale_constrained(configuration)

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test booklet constraints on original size Mixed settings for copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_originalSize_mixed_option_verify_booklet_constrained
    +test:
        +title:test_copy_ui_originalSize_mixed_option_verify_booklet_constrained
        +guid:a44d5458-31d2-4bf9-ba68-eaba61e53370
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A3 & ScannerInput = AutomaticDocumentFeeder & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_originalSize_mixed_option_verify_booklet_constrained(scan_emulation, job, spice, net, cdm, udw, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)

        logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
        job.bookmark_jobs()
        logging.info("Go to copy screen")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        logging.info("set original size to Mixed")
        copy_job_app.select_original_size("MIXED_LETTER_LEDGER")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_booklet_constrained(net)
        copy_job_app.select_original_size("MIXED_LETTER_LEGAL")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_booklet_constrained(net)
        copy_job_app.select_original_size("MIXED_A4_A3")
        logging.info("Verify that page per sheet option is constrained")
        copy_job_app.verify_copy_booklet_constrained(net)

        logging.info("Back to copy screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start to copy")
        copy_job_app.start_copy(dial_value=0)
        Copy(cdm, udw).validate_settings_used_in_copy(
            number_of_copies=1,
            tray_setting="auto",
            original_size="com.hp.ext.mediaSize.mixed-a4-a3",
            orientation="portrait",
            content_type="mixed",
            pages_per_sheet="oneUp")
        logging.info("wait until copying complete")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)
        logging.info("check the job state from cdm")
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])
    finally:
        logging.info("back to the home screen")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy booklet format is set to on, Mixed Size Constraint of Original Size is activated
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_booklet_format_verify_mixed_originalSize_constrained
    +test:
        +title:test_copy_ui_option_booklet_format_verify_mixed_originalSize_constrained
        +guid:ebde1879-b467-4906-aadd-355991d5c929
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=MixedLetterLegal & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_booklet_format_verify_mixed_originalSize_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.goto_copy_option_original_size_screen()
        time.sleep(3)
        copy_job_app.verify_original_size_option_constrained("MIXED_LETTER_LEGAL")

        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.select_original_size("MIXED_LETTER_LEGAL")

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(original_size="com.hp.ext.mediaSize.mixed-letter-legal")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy booklet format is set to on, Check Collate Constraint
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_booklet_format_verify_collate_constrained
    +test:
        +title:test_copy_ui_option_booklet_format_verify_collate_constrained
        +guid:bd3b7ca2-4d26-4034-b989-858e87f7c1d7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_booklet_format_verify_collate_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.verify_copy_collate_constrained()

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy booklet format is set to on, Check staple and punch Constraint
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_booklet_format_verify_staple_punch_constrained
    +test:
        +title:test_copy_ui_option_booklet_format_verify_staple_punch_constrained
        +guid:c95b77e4-d405-4f39-95d6-fe3a4ba9d1a9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A3 & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff & ProductSpecSupported=Finisher

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_booklet_format_verify_staple_punch_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.verify_copy_staple_constrained()
        copy_job_app.verify_copy_punch_constrained()

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(
            media_source='adf',
            booklet_format='leftEdge',
            pages_per_sheet='twoUp',
            output_plex_mode="duplex")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy foldAndStitch is set to on, custom is not constrained
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_verify_fold_and_stitch_custom_constrained
    +test:
        +title:test_copy_ui_option_verify_fold_and_stitch_custom_constrained
        +guid:4ab728e5-de34-43a5-a718-110f9d2e4b41
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff & ADFMediaSize=A4Landscape

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_verify_fold_and_stitch_custom_constrained(scan_emulation, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()

        logging.info("set default options and verify borders on each page constrained")
        copy_job_app.verify_copy_fold_and_stitch_custom_constrained(True)
        
        logging.info("Set booklet format to on.")
        copy_job_app.select_booklet_option('foldAndStitch')

        logging.info("set booklet format and verify borders on each page constrained")
        copy_job_app.verify_copy_fold_and_stitch_custom_constrained(False)

        logging.info("Set borders on each page to on.")
        copy_job_app.select_booklet_option('foldAndStitch_Custom')

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()

        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet = "saddleStitch")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy foldAndStitch is set to on, Check staple and punch Constraint
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_fold_and_stitch_verify_staple_punch_constrained
    +test:
        +title:test_copy_ui_option_fold_and_stitch_verify_staple_punch_constrained
        +guid:c0ae543f-9566-4951-9b8e-8b85ba83a0f3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A3 & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff & ProductSpecSupported=Finisher

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_fold_and_stitch_verify_staple_punch_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('foldAndStitch')
        copy_job_app.verify_copy_staple_constrained()
        copy_job_app.verify_copy_punch_constrained()

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet = "saddleStitch")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy foldAndStitch is set to on, Check fold Constraint
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-208846
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_fold_and_stitch_verify_fold_constrained
    +test:
        +title:test_copy_ui_option_fold_and_stitch_verify_fold_constrained
        +guid:74f966f2-81d3-4ec8-84be-bf83fc2cec78
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ADFMediaSize=A3 & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff & ProductSpecSupported=Finisher

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_option_fold_and_stitch_verify_fold_constrained(scan_emulation, job, udw, spice, cdm, net, configuration):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)
        copy_job_app = spice.copy_ui()
        logging.info("Go to Copy > Options")
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('foldAndStitch')
        copy_job_app.verify_copy_fold_constrained()

        logging.info("Go back Copy Landing screen")
        copy_job_app.back_to_landing_view()
        logging.info("Start a copy job")
        copy_job_app.start_copy()

        logging.info("Validate copy settings for current job")
        Copy(cdm, udw).validate_settings_used_in_copy(finisher_booklet = "saddleStitch")

        logging.info("Check the copy job complete successfully")
        copy_job_app.wait_for_copy_job_status_toast_or_modal(net, configuration)

    finally:
        spice.goto_homescreen()
 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test plex mode constraints on booklet format on settings for copy
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-184338
    +timeout:600
    +asset:Copy
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_booklet_format_option_verify_plexmode_constrained
    +test:
        +title:test_copy_ui_booklet_format_option_verify_plexmode_constrained
        +guid:7e30e6c4-86ac-4f0f-9b04-ec9f3e8fa8b9
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=BookletFormat & CopyBooklet=BookletFormatOnOff
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_booklet_format_option_verify_plexmode_constrained(scan_emulation, job, spice, net):
    try:
        logging.info("Load 8 pages in ADF")
        scan_emulation.media.load_media('ADF', 8)

        logging.info("Need to get latest jobs from CDM later, so have to book mark job firstly")
        job.bookmark_jobs()
        logging.info("Go to copy screen")
        copy_job_app = spice.copy_ui()
        copy_job_app.goto_copy()
        logging.info("go to options screen")
        copy_job_app.goto_copy_options_list()
        logging.info("set booklet format to on and verify constrained")
        copy_job_app.select_booklet_option('bookletFormat')
        copy_job_app.check_copy_side_constrained(net, "1_1_sided")
        copy_job_app.check_copy_side_constrained(net, "2_1_sided")

        logging.info("Back to copy screen")
        copy_job_app.back_to_landing_view()
    finally:
        logging.info("back to the home screen")
        spice.goto_homescreen()

