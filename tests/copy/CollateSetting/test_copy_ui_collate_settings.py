import logging
from dunetuf.power.power import Power, ActivityMode
import time
import pytest

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting collate as on
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:240
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_widget_collate_type_on
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_collate_type_on
        +guid: e6284d06-83c2-4441-b919-c2dcd223b324
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_collate_type_on(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'collate': 'On'
            }
        loadmedia='ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform copy job with setting collate as off
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_copy_ui_adf_menupage_collate_type_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_menupage_collate_type_off
        +guid: 8ef82b89-9445-4f20-ab8c-86ad18e66875
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
# Disable Autouse of the fixture to avoid PUT call timeout issue in NFT
# Epic to remove this disable autouse: DUNE-241671
@pytest.mark.disable_autouse
def test_copy_ui_adf_menupage_collate_type_off(setup_teardown_homescreen, scan_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'collate': 'off'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify that the 'Collate problem' and collateMorePagesDetected alert show when copies > 1 && collate=on; press 'Cancel' 
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +external_files:
    +test_classification:System
    +name:test_copy_ui_1up_collate_cancel
    +test:
        +title:test_copy_ui_1up_collate_cancel
        +guid:5b73661c-b75b-4e70-ad08-88752837b419
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=BlackOnly & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1up_collate_cancel(job, spice, udw, cdm, net, configuration,scan_emulation):
    try:
        job.bookmark_jobs()
        #udw> ScanDeviceService PUB_setNumScanPages <number>
        scan_emulation.media.load_media('ADF',7)

        #udw> CopyJobService PUB_setMaxPagesToCollate <number>
        udw.mainApp.CopyJobService.setMaxPagesToCollate(5)
    
        copy_job_app = spice.copy_ui()
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        options = {
            'collate': 'on',
            'copies': '3'
            }
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)

        logging.info("Check collate limit warning alert")
        if configuration.familyname != "enterprise":
            copy_job_app.wait_for_collate_limit_warning_alert()
        copy_job_app.more_pages_detected_for_collate_window_cancel_copy_job()

        logging.info("Check the copy job cancelled successfully")
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
    
    finally:
        scan_emulation.media.unload_media('ADF')
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: verify that the 'Collate problem' and collateMorePagesDetected alert show when copies > 1 && collate=on. press 'continue'
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +external_files:
    +test_classification:System
    +name:test_copy_ui_1up_collate_continue
    +test:
        +title:test_copy_ui_1up_collate_continue
        +guid:6888ad26-ae3b-44e1-a9d4-b7e0a2d8043c
        +dut:
            +type:Simulator 
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=BlackOnly & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator         
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1up_collate_continue(job, spice, udw, cdm, net, configuration,scan_emulation):
    try:
        job.bookmark_jobs()
        #ScanDeviceService PUB_setNumScanPages x
        scan_emulation.media.load_media('ADF',7)

        #CopyJobService PUB_setMaxPagesToCollate x
        udw.mainApp.CopyJobService.setMaxPagesToCollate(5)
    
        copy_job_app = spice.copy_ui()
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        options = {
            'collate': 'on',
            'copies': '3'
            }
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
 
        logging.info("Check collate limit warning alert")
        if configuration.familyname != "enterprise":
            copy_job_app.wait_for_collate_limit_warning_alert()
        copy_job_app.more_pages_detected_for_collate_window_continue_copy_job()
        # close the 'collate problem' window again
        if configuration.familyname != "enterprise":
            copy_job_app.wait_for_collate_limit_warning_alert()
        # Cancel is necessary on the sim (for now)
        copy_job_app.more_pages_detected_for_collate_window_cancel_copy_job()
        
        logging.info("Check the copy job cancelled successfully")
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}])
    finally:
        scan_emulation.media.unload_media('ADF')
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify that the 'Collate problem' and collateMorePagesDetected alert is not shown when Collate is Off in ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-52016
    +timeout:400
    +asset:Copy
    +test_framework:TUF
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +external_files:
    +test_classification:System
    +name:test_copy_ui_when_collate_off
    +test:
        +title:test_copy_ui_when_collate_off
        +guid:cf09d4f8-b355-42e9-a633-ef6bcc68a315
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator           
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_when_collate_off(scan_emulation, job, spice, udw, cdm, net, configuration):
    try:
        scan_emulation.media.load_media(media_id='ADF')
        job.bookmark_jobs()
        #ScanDeviceService PUB_setNumScanPages 30
        udw.mainApp.ScanDeviceService.setNumScanPages(30)
    
        copy_job_app = spice.copy_ui()
        logging.info("Set number of copies as 2, set collate to off")
       
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        options = {
            'collate': 'off',
            'copies': '2'
            }
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)

        logging.info("Check the copy job complete successfully")
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}])

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify the copy job can be completed without error with settings collate as on and 1_2_sided with original size letter.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-141772
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name: test_copy_ui_adf_collate_on_2copies_sides_1_2_sided_size_letter
    +test:
        +title: test_copy_ui_adf_collate_on_2copies_sides_1_2_sided_size_letter
        +guid: 0e2a5127-011d-4cb6-a679-7f62e64d5227
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=Collation & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_collate_on_2copies_sides_1_2_sided_size_letter(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    try:
        logging.info("Set number of scan pages as 20")
        udw.mainApp.ScanDeviceService.setNumScanPages(20)
        copy_job_app = spice.copy_ui()
        options = {
            'collate': 'On',
            'copies': '2',
            'sides': '1_2_sided', 
            'size' : 'Letter'
            }
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify the copy job can be completed without error with settings collate as on and 2_1_sided with original size letter.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-141772
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name: test_copy_ui_adf_collate_on_2copies_sides_2_1_sided_size_letter
    +test:
        +title: test_copy_ui_adf_collate_on_2copies_sides_2_1_sided_size_letter
        +guid: 89c19060-e803-4635-9b1f-3a98257df13f
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & Copy=Collation & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_collate_on_2copies_sides_2_1_sided_size_letter(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    job.clear_joblog()
    try:
        logging.info("Set number of scan pages as 10")
        udw.mainApp.ScanDeviceService.setNumScanPages(10)
        copy_job_app = spice.copy_ui()
        options = {
            'collate': 'On',
            'copies': '2',
            'sides': '2_1_sided', 
            'size' : 'Letter'
            }
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        spice.goto_homescreen()
        spice.wait_ready()
