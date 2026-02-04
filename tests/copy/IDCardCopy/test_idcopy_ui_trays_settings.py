from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.emulation.print.tray import *
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform idcopy job with Trays as Tray1.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_idcopy_ui_flatbed_landingpage_tray1
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_tray1
        +guid:ee66acc7-05a8-4e0c-b67d-ecda836287c1
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=IDCopy & Copy=PaperTray & MediaInputInstalled=Tray1

    +overrides:
        +ProA4:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_tray1(cdm, media, spice, job, udw, net, tray, print_emulation):
    job.bookmark_jobs()
    try:
        tray1= MediaInputIds.Tray1.name
        print_emulation.tray.empty(tray1)
        print_emulation.tray.load(tray1, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Low.name)
        try:
            cdm.alerts.wait_for_alerts('sizeType',1)
            media.alert_action(category='sizeType', response='ok')
        except:
            logging.debug("SizeType Alert does not appear. Paper is already loaded in tray1.")
        tray.configure_tray("tray-1","na_letter_8.5x11in","stationery")
        
        copy_job_app = spice.copy_ui()
        options = {
            'tray': 'Tray 1'
        }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform idcopy job with Trays as Tray2.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_idcopy_ui_flatbed_menupage_tray2
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_menupage_tray2
        +guid:9927399c-4c78-4d19-9445-d35935ef42a5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=IDCopy & Copy=PaperTray & MediaInputInstalled=Tray2
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_menupage_tray2(spice, job, udw, net, tray): 
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'tray': 'Tray 2'
        }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardMenuPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 
		

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform idcopy job with Trays as Tray3.
    +test_tier: 3
    +is_manual: False
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +external_files:
    +test_classification:System
    +name: test_idcopy_ui_flatbed_landingpage_tray3
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_idcopy_ui_flatbed_landingpage_tray3
        +guid:649445f0-ab18-431d-a374-0a20efa7c443
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Copy=IDCopy & Copy=PaperTray &  MediaInputInstalled=Tray3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_idcopy_ui_flatbed_landingpage_tray3(spice, job, udw, net, tray): 
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'tray': 'Tray 3'
        }
        loadmedia = 'Flatbed'
        copy_path = 'IDCardLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tray.reset_trays() 
