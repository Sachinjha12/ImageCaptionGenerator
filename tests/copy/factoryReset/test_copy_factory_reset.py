import logging
import time

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify that the original size setting is reset to default after factory reset
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-221697
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_factory_reset_verify_options
    +test:
        +title:test_copy_factory_reset_verify_options
        +guid:c7cbc7a9-b4f8-416e-966c-43a1cd98e92c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & PrintEmulation=HighFidelity & ADFMediaSize=AnySize
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:800
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_factory_reset_verify_options(spice, net,udw,cdm,scan_emulation, reset_manager):
    try:
        logging.info("Load ADF and set original size to Letter")
        scan_emulation.media.load_media(media_id='ADF', media_numsheet=1)
        copy_job_app = spice.copy_ui()
        options = {
            'size' : 'Letter'
            }
        loadmedia='ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net,scan_emulation=scan_emulation)
        time.sleep(5)
        logging.info("Save as default copy ticket")
        spice.copy_ui().save_as_default_copy_ticket()

        logging.info("Verify original size setting before factory reset")
        ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
        assert ticket_default_response.status_code == 200
        ticket_default_body = ticket_default_response.json()
        default_src_scan_mediaSize = ticket_default_body["src"]["scan"]["mediaSize"]
        assert default_src_scan_mediaSize == "na_letter_8.5x11in", "Wrong original size setting"

        logging.info("Reset to factory defaults")
        RESET_LEVEL = reset_manager.reset_level.factoryData
        reset_manager.reset_printer(RESET_LEVEL)
        reset_manager.wait_for_device_ready()

        logging.info("Verify original size setting after factory reset")
        ticket_default_response = cdm.get_raw(cdm.JOB_TICKET_COPY)
        assert ticket_default_response.status_code == 200
        ticket_default_body = ticket_default_response.json()
        default_src_scan_mediaSize = ticket_default_body["src"]["scan"]["mediaSize"]
        assert default_src_scan_mediaSize == "any", "Wrong original size setting"

    finally:
        spice.goto_homescreen()


