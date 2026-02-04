import logging
import pytest
import time
from typing import ClassVar

from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.job.job import Job


def goto_paper_selection_paper_size(self, spice, to_select_item):
    self.goto_copy()
    self.goto_copy_options_list()
    self.homemenu.menu_navigation(spice, CopyAppWorkflowObjectIds.view_copySettingsView, CopyAppWorkflowObjectIds.list_copySettings_paperSelection, select_option = False, scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
    self.go_to_paper_selection()
    self.goto_copy_paper_size_screen()
    # self.spice.wait_for("#copy_paperSelectionMenuList #paperSizeSelection", timeout=9.0).mouse_click()
    time.sleep(10)

    self.workflow_common_operations.goto_item(to_select_item, 
        CopyAppWorkflowObjectIds.view_copySettings_paperSelection_paperSize, 
        scrollbar_objectname=CopyAppWorkflowObjectIds.copy_papersize_scrollbar,
        select_option=False) 
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test copy job after paper size is changed in copy app settings (match original size)
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_paper_selection_match_original_size
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_paper_selection_match_original_size
        +guid:278e474b-09a8-4cab-8d80-f1eba8099bd2
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_job_with_paper_selection_match_original_size(spice, cdm, udw, job, scan_emulation):
    try:   
        scan_emulation.media.load_media('ADF',1)
        copy_job_app = spice.copy_ui()
        job.bookmark_jobs()
        
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        # set paper size
        to_select_item = CopyAppWorkflowObjectIds.row_media_size_any
        goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
        custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
        custom_button.mouse_click()
        
        # start copy job
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()

        # Wait for the job to complete and get the job id.
        job_id = job.wait_for_completed_job(last_job_id, job, udw)
        job_id_cdm = job.get_jobid(job_id, guid=True)
        logging.info("jobId is "+ job_id_cdm)

        # check job details in cdm
        command_output = udw.mainApp.JobTicketResourceManager.getAllJobTicketIDs()
        ids = command_output.split('\n')
        last_job_id = ids[len(ids)-1]
        job_ticket = cdm.get(cdm.JOB_TICKET_ENDPOINT + f"/{last_job_id}")
        print(job_ticket['dest']['print']['mediaSize'])
        assert job_ticket['dest']['print']['mediaSize'] == 'any', "Not matched"

        # Go to Homescreen and Job Queue App screen
        spice.goto_homescreen()
        spice.main_app.goto_job_queue_app()

        # Check that the job is in "History" section
        spice.job_ui.goto_job(job_id_cdm)
        assert spice.job_ui.recover_job_status() == "Completed"

        # Check by CDM that the job has passed to history
        job_cdm = job.get_job_from_history_by_id(job_id_cdm)
        assert job_cdm["jobId"] == job_id_cdm

        # Check job details in UI
        assert spice.job_ui.recover_job_type() == "Copy" 
        assert spice.job_ui.recover_job_output_size() == "Letter (8.5x11 in.)"
        """assert spice.job_ui.recover_job_output_size() == spice.job_ui.recover_job_original_size()""" # Letter (8.5x11 in.) // Letter ▭ (8.5x11 in.)

    finally:
        spice.goto_homescreen()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test copy job after paper size is changed in copy app settings (custom size)
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:1200
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_paper_selection_custom_size
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_paper_selection_custom_size
        +guid:7bee9615-681f-405a-a763-55cbf4a3741e
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & ScanMode=Book
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_job_with_paper_selection_custom_size(spice, cdm, udw, job, configuration):
    try:
        test_list = [
            {'unit': 'mm', 'value_x' : 200, 'value_y' : 200},
            {'unit': 'inch', 'value_x' : 7, 'value_y' : 7}
        ]
        for test in test_list:

            unit = test['unit']
            value_x = test['value_x']
            value_y = test['value_y']

            copy_job_app = spice.copy_ui()
            job.bookmark_jobs()

            # check jobId
            job_ids = job.get_recent_job_ids()
            last_job_id = job_ids[len(job_ids) - 1]
            job_ids.clear()

            # set paper size
            to_select_item = CopyAppWorkflowObjectIds.row_media_size_custom
            goto_paper_selection_paper_size(copy_job_app, spice, to_select_item)
            custom_button = copy_job_app.spice.wait_for(to_select_item, timeout = 9.0)
            custom_button.mouse_click()
            copy_job_app.set_copy_custom_size_value(unit, value_x, value_y, configuration)

            # start copy job
            copy_job_app.spice.wait_for("#copy_mediaSizeMenuSelectionList #BackButton", timeout=9.0).mouse_click()
            copy_job_app.go_back_to_setting_from_paper_selection()
            copy_job_app.back_to_landing_view()
            copy_job_app.start_copy()
            if configuration.productname == "camden":
                time.sleep(10)
                copy_job_app.spice.wait_for("#FooterView #FooterViewRight #mainActionButtonOfDetailPanel", timeout=9.0).mouse_click()
        
            # Wait for the job to complete and get the job id.
            job_id = job.wait_for_completed_job(last_job_id, job, udw)
            job_id_cdm = job.get_jobid(job_id, guid=True)
            logging.info("jobId is "+ job_id_cdm)

            # check job details in cdm
            command_output = udw.mainApp.JobTicketResourceManager.getAllJobTicketIDs()
            ids = command_output.split('\n')
            last_job_id = ids[len(ids)-1]
            job_ticket = cdm.get(cdm.JOB_TICKET_ENDPOINT + f"/{last_job_id}")
            assert job_ticket['dest']['print']['mediaSize'] == 'custom', "Not matched"

            copy_job_id = Job.wait_for_completed_job(last_job_id, job, udw)

            # Go to Homescreen and Job Queue App screen
            spice.goto_homescreen()
            Job.verify_job_status_udw(udw, copy_job_id, "COMPLETED", "SUCCESS")

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:test copy job after paper tray is changed in copy app settings (manual feed)
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-143696
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_job_with_paper_selection_tray_manual_feed
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_paper_selection_tray_manual_feed
        +guid:00eb8205-ccc8-4ef1-9baf-dd0866c4d878
        +dut:
            +type:Simulator
            +configuration:DeviceASIC=Tron & DeviceClass=MFP & DeviceFunction=Copy & MediaInputInstalled=ManualFeed
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_job_with_paper_selection_tray_manual_feed(spice, cdm, udw, job):
    try:   
        copy_job_app = spice.copy_ui()
        job.bookmark_jobs()
        
        # check jobId
        job_ids = job.get_recent_job_ids()
        last_job_id = job_ids[len(job_ids) - 1]
        job_ids.clear()

        # set paper tray
        copy_job_app.goto_copy()
        copy_job_app.goto_copy_options_list()
        copy_job_app.homemenu.menu_navigation(spice, 
                                                CopyAppWorkflowObjectIds.view_copySettingsView, 
                                                CopyAppWorkflowObjectIds.list_copySettings_paperSelection, 
                                                select_option = False, 
                                                scrollbar_objectname = CopyAppWorkflowObjectIds.copy_options_scrollbar)
        copy_job_app.go_to_paper_selection()
        copy_job_app.select_paper_tray_option("Manual feed")

        # start & cancel copy job
        copy_job_app.go_back_to_setting_from_paper_selection()
        copy_job_app.back_to_landing_view()
        copy_job_app.start_copy()
        time.sleep(10)
        cancel_btn = copy_job_app.spice.wait_for("#bodyLayoutverticalLayout #Cancel", timeout=9.0)
        cancel_btn.mouse_click()

        # check job details in cdm
        command_output = udw.mainApp.JobTicketResourceManager.getAllJobTicketIDs()
        ids = command_output.split('\n')
        last_job_id = ids[len(ids)-1]
        job_ticket = cdm.get(cdm.JOB_TICKET_ENDPOINT + f"/{last_job_id}")
        assert job_ticket['dest']['print']['mediaSource'] == 'manual', "Not matched"

    finally:
        spice.goto_homescreen()
