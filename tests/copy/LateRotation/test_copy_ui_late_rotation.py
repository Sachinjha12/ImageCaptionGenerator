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
    +purpose:Test copy Late rotation angle for basic job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_basic
    +test:
        +title:test_copy_ui_adf_late_rotation_basic
        +guid:c9286ace-07de-4b78-b543-8284444f771c
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_basic(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',1)
        spice.copy_ui().goto_copy()
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
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for basic job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_flatbed_late_rotation_basic
    +test:
        +title:test_copy_ui_flatbed_late_rotation_basic
        +guid:4441fee9-e8f9-47e3-9151-c953b163c971
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_flatbed_late_rotation_basic(job, spice, scan_emulation, udw, ssh, outputverifier, configuration):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.unload_media('ADF')
        spice.copy_ui().goto_copy()
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        spice.copy_ui().start_copy(adfLoaded=False, familyname=configuration.familyname)
        copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)
        # Verify job is success
        Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

        # Verify the final rotation angle
        outputverifier.save_and_parse_output()
        outputverifier.verify_rotate(Intents.printintent,1)
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for basic job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_1_2sided
    +test:
        +title:test_copy_ui_adf_late_rotation_1_2sided
        +guid:4f1ca86e-7e55-434f-ae0d-2b359e105bdf
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided1To2 & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_1_2sided(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
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
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.long_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for 2_1 sided job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2_1sided
    +test:
        +title:test_copy_ui_adf_late_rotation_2_1sided
        +guid:58e3602e-ab69-493c-ae34-3c597a83d67a
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided2To1 & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2_1sided(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_1_sided")
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
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.portrait)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for 2_2 sided job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2_2sided
    +test:
        +title:test_copy_ui_adf_late_rotation_2_2sided
        +guid:742aaf19-226a-431e-874e-67174e593135
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2Sided2To2 & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2_2sided(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_copy_side("2_2_sided")
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
    +purpose:Test copy Late rotation angle for PagesPersheet 2 job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon

    +name:test_copy_ui_adf_late_rotation_2up
    +test:
        +title:test_copy_ui_adf_late_rotation_2up
        +guid:2d55f184-2264-410a-856d-2fde798a590a
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
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
        outputverifier.verify_plex(Intents.printintent, Plex.simplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.one_sided)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 1_2 sided job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_1_2sided
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_1_2sided
        +guid:f7c4aa4d-043e-48ac-b65f-722e56c280dd
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & Copy=2Sided1To2 & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_1_2sided(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
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
        outputverifier.verify_plex(Intents.printintent, Plex.duplex)
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy Late rotation angle for PagesPersheet 2, 2_2sided job from ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-170613
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:3
    +delivery_team:A3
    +feature_team:A3_ProductCommon
    +name:test_copy_ui_adf_late_rotation_2up_2_2sided
    +test:
        +title:test_copy_ui_adf_late_rotation_2up_2_2sided
        +guid:c141a4ca-a9ff-48db-9b8b-fa4073fe9126
        +dut:
            +type:Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=2PagesPerSheet & Copy=2Sided2To2 & ADFMediaSize=MixedA4A3


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$

"""
def test_copy_ui_adf_late_rotation_2up_2_2sided(job, spice, scan_emulation, udw, ssh, outputverifier):
    try:

        logging.info("Clearing previous generated intents")
        cleanIntents(ssh)
        scan_emulation.media.load_media('ADF',2)
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy()
        spice.copy_ui().goto_copy_options_list()
        spice.copy_ui().select_pages_per_sheet_option(udw, "2")
        spice.copy_ui().select_copy_side("2_2_sided")
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
        outputverifier.verify_content_orientation(Intents.printintent, ContentOrientation.landscape)
        outputverifier.verify_plex_binding(Intents.printintent, PlexBinding.short_edge)
    finally:
        outputverifier.outputsaver.clear_output()
        spice.goto_homescreen()
        spice.wait_ready()

