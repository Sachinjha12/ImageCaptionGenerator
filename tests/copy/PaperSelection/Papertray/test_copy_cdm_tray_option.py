import logging
import pytest
import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.print.print_common_types import MediaInputIds,MediaSize,MediaType,MediaOrientation,TrayLevel
from dunetuf.job.job import Job

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test tray values in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-177486
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_tray_empty_load_paper
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_tray_empty_load_paper
        +guid:8a98dbca-4079-47d7-89b2-2c59a312a4df
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=Tray1 & Copy=IDCopy
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_tray_empty_load_paper(spice, tcl, net,tray,udw,configuration):
    try:
     if configuration.productname in ["eddington", "elion", "marconi/marconisfpdl", "marconi/marconihipdl", "marconi/marconipdl", "marconi/marconihi", "marconi/marconi", "marconi/marconisf", "moreto", "moretohi"]:
        empty_media = "EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {{ idDevice: 1, stateValue: ERROR , statusValues:[ OUT_OF_MEDIA ]  }}"
     else:
        empty_media = "EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {{ idDevice: 1, stateValue: INFORM, statusValues:[ ALMOST_OUT_OF_MEDIA ] }}"
     tcl.execute(empty_media, timeout = 200)  
     time.sleep(3)
     udw.mainApp.ScanMedia.loadMedia("ADF")
     udw.mainApp.ScanDeviceService.setNumScanPages(1)
     spice.copy_ui().goto_copy()
     spice.copy_ui().goto_copy_options_list()
     spice.copy_ui().go_to_paper_selection()
     spice.copy_ui().select_paper_tray_option("Tray 1")
     spice.copy_ui().go_back_to_setting_from_paper_selection()
     spice.copy_ui().back_to_landing_view()
     spice.copy_ui().start_copy()
     spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
     spice.copy_ui().tray_empty_load_paperscreen("ok")

    finally:
       remove_empty_paper_command = "EngineSimulatorUw executeSimulatorAction MEDIA setDeviceStatus {{ idDevice: 1, stateValue: OK, statusValues:[ READY ] }}"
       tcl.execute(remove_empty_paper_command)
       spice.goto_homescreen()
       tray.reset_trays()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test tray values in copy app settings
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-221697
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_tray_empty_load_paper1
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_tray_empty_load_paper1
        +guid:9f38d764-3b31-4ccb-ac66-182143928700
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & TraySettings=TrayPriority
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:800
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_tray_empty_load_paper1(spice, net, job, udw, media, configuration, scan_emulation, print_emulation):
    job_ids = job.get_recent_job_ids()
    last_job_id = job_ids[len(job_ids) - 1]
    job_ids.clear()
    try:
        scan_emulation.media.load_media('ADF',1)
        tray2= MediaInputIds.Tray2.name
        print_emulation.tray.open(tray2)
        print_emulation.tray.empty(tray2)
        print_emulation.tray.close(tray2)
        media.alert_action(category='sizeType', response='ok')
        time.sleep(3)

        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().go_to_paper_selection()
        spice.copy_ui().select_paper_tray_option("Tray 2")
        spice.copy_ui().go_back_to_setting_from_paper_selection()
        spice.copy_ui().back_to_landing_view()
        spice.copy_ui().start_copy()
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting')
        spice.copy_ui().tray_empty_load_paperscreen("Hide")
        current_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_button)
        current_button.mouse_click()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        Job.verify_job_status_udw(udw, copy_job_id, "CANCELING", "COMPLETED")

        print_emulation.tray.open(tray2)
        print_emulation.tray.load(tray2, MediaSize.Letter.name, MediaType.Plain.name, MediaOrientation.Default.name, TrayLevel.Full.name)
        print_emulation.tray.close(tray2)

    finally:
        spice.goto_homescreen()
        print_emulation.tray.reset_trays()