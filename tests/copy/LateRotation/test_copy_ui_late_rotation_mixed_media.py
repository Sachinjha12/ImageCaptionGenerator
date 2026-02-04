from dunetuf.copy.copy import *
import pytest
import logging
from dunetuf.print.output.intents import Intents, PlexSide, ContentOrientation, PlexBinding, Plex
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
Clean the intents
"""
def cleanIntents(ssh):
    command = "rm -f /tmp/PrintIntent*json"
    ssh.run(command)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 2_2sided, landscape, mixed media job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media
        +guid:b2a25e29-ca04-4d16-987d-56e73d72f12a
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=MixedA4A3 & Copy=2PagesPerSheet & Copy=2Sided2To2 & ScanSettings=Orientation


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',4)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().select_original_size("MIXED_LETTER_LEGAL")
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

        # Verify the final rotation angle
        outputverifier.save_and_parse_output()
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 0)
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 1)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 2_2 sided, landscape, mixed mdeia, pageFlipped job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media_pageflipped
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media_pageflipped
        +guid:7a2a042d-88e0-4b29-8fdc-47460d8b7d21
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=MixedA4A3 & Copy=2PagesPerSheet & Copy=2Sided2To2 & ScanSettings=Orientation


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_mixed_media_pageflipped(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().set_copy_2sided_flip_up_options("on")
        spice.copy_ui().select_original_size("MIXED_LETTER_LEGAL")
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

        # Verify the final rotation angle
        outputverifier.save_and_parse_output()
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 0)
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 1)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for landscape, mixed media copy job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_landscape_mixed_media
    +test:
        +title:test_copy_ui_adf_late_rotation_landscape_mixed_media
        +guid:f0f5675b-4e1f-4cc4-934d-bfa78acbe8dc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=MixedA4A3 & ScanSettings=Orientation


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_landscape_mixed_media(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().select_original_size("MIXED_LETTER_LEGAL")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

        # Verify the final rotation angle
        outputverifier.save_and_parse_output()
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 0)
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for mixed media copy job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_mixed_media
    +test:
        +title:test_copy_ui_adf_late_rotation_mixed_media
        +guid:3a9e11b0-4c12-401e-88e2-eac6ebfbc61f
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_mixed_media(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("MIXED_LETTER_LEGAL")
        spice.copy_ui().back_to_landing_view()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy()
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

        # Verify the final rotation angle
        outputverifier.save_and_parse_output()
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 0)
        outputverifier.verify_per_page_rotate(Intents.printintent,1, 1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

