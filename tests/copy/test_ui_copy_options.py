from logging import exception
import time
import uuid
from dunetuf.cdm.CdmShortcuts import CDMShortcuts
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy
import json
import pprint
import logging
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel

def reset_trays(tray, print_emulation):
    # load and configure the installed trays with default values(letter and plain)
    tray_list = print_emulation.tray.get_installed_trays()
    for tray_id in tray_list:
        print_emulation.tray.capacity_unlimited(tray_id)
        if tray_id == MediaInputIds.Tray1.name:
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
        else:
            print_emulation.tray.open(tray_id)
            print_emulation.tray.load(tray_id, MediaSize.Letter.name)
            print_emulation.tray.close(tray_id)
    # configure the trays with default values using CDM call
    tray.reset_trays()

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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy options Paper tray, Paper Type, lighter/Darker, Resize, collate
    +test_tier:1
    +is_manual:False
    +reqid:DUNE
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_tray_exposure_paper_type_sides2
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_tray_exposure_paper_type_sides2
        +guid:3f4a4c61-d2ce-40d2-bc7a-64cad9b5a4a1
        +dut:
            +type:Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=2Sided1To2 & Copy=ResizeCustom & CopyOutputScale=FullPage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_tray_exposure_paper_type_sides2(scan_emulation, print_emulation, tray, media, job, net, udw, spice, cdm):

    # check jobId
    scan_emulation.media.load_media(media_id='ADF')
    print_emulation.tray.empty(MediaInputIds.Tray1.name)
    print_emulation.tray.load(MediaInputIds.Tray1.name, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name, status_values='READY, OCCUPIED')
    try:
        cdm.alerts.wait_for_alerts('sizeType',1)
        media.alert_action(category='sizeType', response='ok')
    except:
        logging.debug("SizeType Alert does not appear. Paper is already loaded in tray1.")
    tray.configure_tray("tray-1","na_letter_8.5x11in","stationery")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy2", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_options_list()

        # set copy options
        spice.copy_ui().select_copy_side("1_2_sided")
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().select_paper_type_option("Plain")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_scan_settings_lighter_darker(8)
        spice.copy_ui().select_resize_option("FullPage(91%)")
        spice.copy_ui().change_collate()

        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()

        # Verify ticket values
        ticket_default_body = Copy.get_copy_default_ticket(cdm)
        assert 'simplex' == ticket_default_body["src"]["scan"]["plexMode"]
        assert 'duplex' == ticket_default_body["dest"]["print"]["plexMode"]
        assert 'tray-1' == ticket_default_body["dest"]["print"]["mediaSource"]
        #assert 'na_legal_8.5x14in' == ticket_default_body["dest"]["print"]["mediaSize"]
        assert 'stationery' == ticket_default_body["dest"]["print"]["mediaType"]
        assert 8 == ticket_default_body["pipelineOptions"]["imageModifications"]["exposure"]
        assert 'uncollated' == ticket_default_body["dest"]["print"]["collate"]

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        if spice.signIn.get_sign_in_status() == "Sign Out":
            spice.signIn.goto_universal_sign_in("Sign Out")
            spice.is_HomeScreen()
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)
        reset_trays(tray, print_emulation)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy options Paper tray, Paper Type, lighter/Darker, Resize, collate
    +test_tier:1
    +is_manual:False
    +reqid:DUNE
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_tray_exposure_paper_type_sides
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_tray_exposure_paper_type_sides
        +guid:1780cb17-b8db-4257-a30a-23abe6095534
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & Copy=2Sided1To2 & Copy=ResizeCustom & CopyOutputScale=FullPage
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_tray_exposure_paper_type_sides(job, net, udw, spice, cdm):

    # check jobId
    udw.mainApp.ScanMedia.loadMedia("ADF")
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)

    try:
        # For workflow, default quickset will not displayed in quickset list view, need to creat at least one quickset.
        csc = CDMShortcuts(cdm, net)
        shortcut_id = str(uuid.uuid4())
        # Create shortcut : provide shortcutName,shortcutId,source,destinations,action,copyAllowed,isFactory: bool
        csc.create_custom_shortcut("MyCopy2", shortcut_id, "scan", [
                                   "print"], "open", "true", False, csc.JobTicketType.COPY)

        spice.copy_ui().goto_copy()
        spice.copy_ui().verify_selected_quickset_name(net, 'cDefault')
        spice.copy_ui().goto_copy_options_list()

        # set copy options
        spice.copy_ui().select_copy_side("1_2_sided")
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_tray_option("Tray 1")
        spice.copy_ui().select_paper_type_option("Plain")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().select_scan_settings_lighter_darker(8)
        spice.copy_ui().select_resize_option("FullPage(91%)")
        spice.copy_ui().change_collate()

        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()

        # Verify ticket values
        ticket_default_body = Copy.get_copy_default_ticket(cdm)
        assert 'simplex' == ticket_default_body["src"]["scan"]["plexMode"]
        assert 'duplex' == ticket_default_body["dest"]["print"]["plexMode"]
        assert 'tray-1' == ticket_default_body["dest"]["print"]["mediaSource"]
        #assert 'na_legal_8.5x14in' == ticket_default_body["dest"]["print"]["mediaSize"]
        assert 'stationery' == ticket_default_body["dest"]["print"]["mediaType"]
        assert 8 == ticket_default_body["pipelineOptions"]["imageModifications"]["exposure"]
        assert 'uncollated' == ticket_default_body["dest"]["print"]["collate"]

        spice.copy_ui().start_copy()

        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        if spice.signIn.is_signed_in():
            spice.signIn.goto_universal_sign_in("Sign Out")
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)
        # delete previously added shorcut
        csc.delete_shortcut(shortcut_id)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test copy options ContentType, ColorMode
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_color_auto_detect
    +test:
        +title:test_copy_ui_option_color_auto_detect
        +guid:30686243-9aa1-4a17-b920-b2bb118aa21f
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_color_auto_detect(scan_emulation, job, udw, spice, cdm, configuration):
    scan_emulation.media.load_media(media_id='ADF') # For Simulator default scan resouce is ADF, then need to reload ADF end of testing    
    # check jobId
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    original_ticket_default_body = Copy.get_copy_default_ticket(cdm)

    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        # set copy options
        spice.copy_ui().select_content_type("Photograph")
        if cdm.device_feature_cdm.is_color_supported():
            spice.copy_ui().select_color_mode("Automatic")
        # spice.copy_ui().select_quality_option("Best")

        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().save_as_default_copy_ticket()
        # Verify ticket values
        ticket_default_body = Copy.get_copy_default_ticket(cdm)
        assert 'photo' == ticket_default_body["src"]["scan"]["contentType"]
        if cdm.device_feature_cdm.is_color_supported():
            assert 'autoDetect' == ticket_default_body["src"]["scan"]["colorMode"]
        # assert 'best' == ticket_default_body["dest"]["print"]["printQuality"]
        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        spice.signIn.goto_universal_sign_in("Sign Out")
        Copy.reset_copy_default_ticket(cdm, original_ticket_default_body)


def source_destination(source,dest):
    return {'src': {source:{}}, 'dest': {dest:{}} }



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test_copy_ui_option_paperSize_constrained
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-99493
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_option_paperSize_constrained
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_option_paperSize_constrained
        +guid:d3a8a688-c869-4ace-a404-2c98610249cf
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScanColorMode=Automatic & Copy=Color & MediaSizeSupported=AnyCustom
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator        
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_option_paperSize_constrained(spice, cdm):
    
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
            spice.copy_ui().select_media_size_option_constrained(paper_size_object_name)
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
    finally:
        spice.goto_homescreen()
