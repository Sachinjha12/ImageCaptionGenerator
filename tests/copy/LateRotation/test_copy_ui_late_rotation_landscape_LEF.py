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
    +purpose:Test copy Late rotation angle for PagesPersheet 2 and landscape job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_landscape
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_landscape
        +guid:b68ea3af-3feb-42f3-b086-7dd707b934b8
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & ScanSettings=Orientation & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_landscape(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
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
        outputverifier.verify_rotate(Intents.printintent,1)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 1_2sided , landscape job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_1_2sided_landscape
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_1_2sided_landscape
        +guid:59dd377a-2e22-45af-b0c4-87a8f8a167bd
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & Copy=2Sided1To2 & ScanSettings=Orientation & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_1_2sided_landscape(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        spice.copy_ui().select_copy_side("1_2_sided")
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
        outputverifier.verify_rotate(Intents.printintent,1)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2 2_2 sided, landscape job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape
        +guid:a47e44bf-52bf-448b-89f5-d49de428f4b9
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & Copy=2Sided2To2 & ScanSettings=Orientation & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_2_2sided_landscape(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        spice.copy_ui().select_copy_side("2_2_sided")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for landscape copy job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_landscape
    +test:
        +title:test_copy_ui_adf_late_rotation_landscape
        +guid:bbf68276-fe82-437e-9cbb-2a883693f8e2
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanSettings=Orientation & ADFMediaSize=MixedA4A3 & Copy=OriginalSize & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_landscape(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_original_size("Letter_SEF")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for landscape copy LEF job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_landscape_LEF
    +test:
        +title:test_copy_ui_adf_late_rotation_landscape_LEF
        +guid:88a6c55d-84e6-4941-9266-8739dccfa68f
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ScanSettings=Orientation & ADFMediaSize=MixedA4A3 & Copy=OriginalSize & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_landscape_LEF(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().select_original_size("Letter")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 2_2sided, landscape, LEF job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_LEF
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_LEF
        +guid:688ba2ca-f487-44d4-9efc-2bce31b29ecc
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & Copy=2Sided2To2 & ScanSettings=Orientation & ADFMediaSize=MixedA4A3 & Copy=OriginalSize & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_2_2sided_landscape_LEF(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        spice.copy_ui().select_copy_side("2_2_sided")
        spice.copy_ui().set_content_orientation_settings(CopyAppWorkflowObjectIds.orientation_landscape_option)
        spice.copy_ui().select_original_size("Letter")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for 1_2 sided, LEF job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_1_2sided_LEF
    +test:
        +title:test_copy_ui_adf_late_rotation_1_2sided_LEF
        +guid:7c6566d7-0be7-49d9-ba76-bd4b9e2262fd
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided1To2 & ScanSettings=Orientation & ADFMediaSize=MixedA4A3 & Copy=OriginalSize & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_1_2sided_LEF(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("1_2_sided")
        spice.copy_ui().select_original_size("Letter")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, LEF job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_LEF
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_LEF
        +guid:bc804a55-fdd9-42ae-8391-2e162ed47b03
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & ScanSettings=Orientation & ADFMediaSize=MixedA4A3 & Copy=OriginalSize & Copy=PaperSize


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_LEF(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        spice.copy_ui().select_original_size("Letter")
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
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

