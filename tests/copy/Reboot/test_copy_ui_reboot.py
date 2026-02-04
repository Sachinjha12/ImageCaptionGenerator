import logging
from dunetuf.copy.copy import *
from dunetuf.power.power import Power
from dunetuf.control.device_status import DuneDeviceStatus


N_COPIES = 5
SINGLE_COPY_COUNT_INCREMENT = 1
SCAN_WAIT_TIMEOUT = 30.0
from time import sleep

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: navigate to copy scree update no of copies and reboot,verify options after reboot
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_reboot_verify_options
    +test:
        +title:test_copy_ui_reboot_verify_options
        +guid: 814236c8-c4e1-4879-9599-085b6fca2115
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

# Test name
def test_copy_ui_reboot_verify_options(spice, net,udw,cdm,setup_teardown_with_copy_job):
    try:
     spice.copy_ui().goto_copy()
     spice.copy_ui().ui_copy_set_no_of_pages(N_COPIES)
     spice.copy_ui().save_as_default_copy_ticket()
     Power(udw).power_cycle()
     # ssh.run("reboot")
     sleep(60)
     # wait for system to reboot
     device_status = DuneDeviceStatus(net.ip_address,"")
     result = device_status.device_ready(300)
     assert all(result.values())
     ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
     assert ticket_default_response.status_code == 200
     ticket_default_body = ticket_default_response.json()
     default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"]
     assert default_dest_print_copies == N_COPIES

    finally:
     spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify once setting as Any size shall be retained after reboot
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +test_classification:System
    +name:test_copy_ui_reboot_verify_originalsize_options
    +test:
        +title:test_copy_ui_reboot_verify_originalsize_options
        +guid:811232f4-2e6c-4bc0-990e-9cc8780e0e09
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=AnySize
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_reboot_verify_originalsize_options(spice, udw, cdm, job, net, configuration):
    job.bookmark_jobs()
    job.clear_joblog()
    udw.mainApp.ScanMedia.unloadMedia("ADF")
    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        logging.info("Set Original size as Any")
        spice.copy_ui().select_original_size('Any')
        spice.copy_ui().back_to_landing_view()
        Power(udw).power_cycle()
        sleep(60)
        # wait for system to reboot
        device_status = DuneDeviceStatus(net.ip_address,"")
        result = device_status.device_ready(300)
        assert all(result.values())
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        mediaSize = "Any"
        if (configuration.familyname == "homepro"):
           mediaSize = "Letter"
        spice.copy_ui().verify_copy_mediasize_selected_option(net, "original", mediaSize)
        spice.copy_ui().back_to_landing_view()
    finally:
       udw.mainApp.ScanMedia.loadMedia("ADF")
       spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Verify copy job status once device is rebooted
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-141772
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_reboot_verify_copyjob_canceled
    +test:
        +title:test_copy_ui_reboot_verify_copyjob_canceled
        +guid:ca64f0c1-bea0-492d-a51d-64c8f169f208
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_reboot_verify_copyjob_canceled(spice, udw, cdm, job, net, configuration):
    job.bookmark_jobs()
    job.clear_joblog()
    udw.mainApp.ScanMedia.loadMedia("ADF")
    try:
        # Go to copy app and start copy job
        spice.copy_ui().goto_copy()    
        spice.copy_ui().change_num_copyApp_copies(99)
        spice.copy_ui().start_copy()
        spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='Starting', timeout= 120)
        Power(udw).power_cycle()
        sleep(60)
        # wait for system to reboot
        device_status = DuneDeviceStatus(net.ip_address,"")
        result = device_status.device_ready(300)
        assert all(result.values())
        job.wait_for_no_active_jobs()
        job_id = job.get_last_job_id_cdm()
        logging.info('job_id,', job_id)
        #Read Data from stats Job
        ENDPOINT= cdm.JOB_STAT_ENDPOINT + job_id
        response = cdm.get_raw(ENDPOINT)
        assert response.status_code==200, 'Unexpected response'
        cdm_response = response.json()
        logging.info(cdm_response)
        assert cdm_response['jobInfo']['jobCompletionState'] == 'cancelled' , 'Job was not cancelled'

    finally:
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: navigate to copy scree update no of copies and reboot,verify options after reboot on engine
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-29871
    +timeout:500
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +name:test_copy_ui_reboot_verify_options_engine
    +test:
        +title:test_copy_ui_reboot_verify_options_engine
        +guid: 280165b6-73e8-42ed-b902-59270927734e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_reboot_verify_options_engine(spice, net,udw,cdm,setup_teardown_with_copy_job, reset_manager):
    try:
     spice.copy_ui().goto_copy()
     spice.copy_ui().ui_copy_set_no_of_pages(N_COPIES)
     spice.copy_ui().save_as_default_copy_ticket()
     logging.info("Reboot the device and wait device ready")
     reset_manager.reboot_printer()
     reset_manager.wait_for_device_ready()
     ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
     assert ticket_default_response.status_code == 200
     ticket_default_body = ticket_default_response.json()
     default_dest_print_copies = ticket_default_body["dest"]["print"]["copies"]
     assert default_dest_print_copies == N_COPIES

    finally:
     spice.goto_homescreen()
