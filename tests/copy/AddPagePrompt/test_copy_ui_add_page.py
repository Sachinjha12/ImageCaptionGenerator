import logging
import time
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt in copy using more than one page with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done
        +guid:742c0928-5634-40c3-8a4c-2b71445ed4c4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt & Copy=Collation

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'On',
            'copies': '3'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_finish()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Load media from ADF
        scan_emulation.media.load_media('ADF',1)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt more than one page with collate Off
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done_collate_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done_collate_off
        +guid:9d676b3a-f3cd-4a0b-af0d-2d140abe1c79
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_done_collate_off(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'off',
            'copies': '3'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_finish()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt cancel scenario
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_cancel
        +guid:1108e69d-7bf1-4e88-9668-7a05ffeb56c0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_scan_and_cancel(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'off'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        time.sleep(1) # To find cancel button in next prompt
        spice.copy_ui().duplex_add_page_pop_up_cancel()
        time.sleep(1) # To find cancel button in next prompt
        spice.copy_ui().add_page_pop_up_cancel_no()
        time.sleep(1) # To find cancel button in next prompt
        spice.copy_ui().duplex_add_page_pop_up_cancel()
        time.sleep(1) # To find cancel button in next prompt
        spice.copy_ui().add_page_pop_up_cancel_yes()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt more than 10 pages scenario with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 350
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_more_than_10_pages
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_more_than_10_pages
        +guid:f979bee9-3da3-4de8-b4aa-a6f64a825af7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt & Copy=Collation

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_more_than_10_pages(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'On',
            'copies': '3'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than 10pages
        for _ in range(9):
            time.sleep(2)
            spice.copy_ui().duplex_add_page_pop_up_add_more()
        
        spice.copy_ui().duplex_add_page_pop_up_finish()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt noResponse/timeout scenario
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 800
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_and_no_response
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_and_no_response
        +guid:1dcd8cbb-2602-4c7e-a829-6ec057430ea8
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_and_no_response(job, spice, net, udw,scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'off'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        logging.info("Waiting for 180 seconds to inactive/timeout the add page pop up")
        time.sleep(240)
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 2_1Sided addPage prompt in copy using 2 pages per sheet with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161762
    +timeout: 450
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet
        +guid:de04dd51-44fe-4690-a595-ffe3ff765b78
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & FlatbedSettings=DuplexPrompt & Copy=Collation & Copy=2PagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'collate': 'On',
            'copies': '3',
            'pagesPerSheet': '2'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_finish()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type":"copy","status":"success"}],time_out=120)
        
    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt in copy using more than one page with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done
        +guid:c6c6fd5b-b23d-4867-864a-93ea19c36c18
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=Collation

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done(job, spice, net, udw,cdm, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'On',
            'copies': '3',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt more than one page with collate Off
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off
        +guid:ebd14c79-c796-49be-9f2b-15f245f4cda8
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off(job, spice, net, udw,cdm, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'off',
            'copies': '3',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_2Sided addPage prompt in copy using more than one page with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_2Sided_add_page_scan_more_than_one_page_and_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_2Sided_add_page_scan_more_than_one_page_and_done
        +guid:392cb601-9aa9-413d-833f-6f5d05153730
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=Collation

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_2Sided_add_page_scan_more_than_one_page_and_done(job, spice, net,cdm, udw,scan_emulation):
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('Flatbed', 1)
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_2_sided',
            'collate': 'On',
            'copies': '3',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)

        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}], time_out=120)

    finally:
        # Unload media from ADF
        # udw.mainApp.ScanMedia.loadMedia("ADF")
        scan_emulation.media.load_media('ADF', 1)
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt with 2 pages per sheet with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 350
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet
        +guid:421f88c8-cbf0-4f21-95f0-84595b83b309
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=Collation & Copy=2PagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_2pages_per_sheet(job, spice, net, udw, cdm, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'On',
            'copies': '3',
            'pagesPerSheet': '2'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}], time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the Flatbed 1_1Sided addPage prompt in copy using more than one page with 2 pages per sheet and collate Off
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 350
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off_2pages_per_sheet
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off_2pages_per_sheet
        +guid:c032d73e-5933-46dd-b04c-ac6eae8a3d81
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=2PagesPerSheet

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_done_collate_off_2pages_per_sheet(job, spice, net, udw,cdm, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'off',
            'copies': '3',
            'pagesPerSheet': '2'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}], time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt cancel scenario
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_cancel
        +guid:3007d95f-8276-4c12-8448-c85e00be8995
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_one_page_and_cancel(job, spice, net, udw,cdm, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('Flatbed', 1)   
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'off',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than one page
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_cancel()
        spice.copy_ui().add_page_pop_up_cancel_no()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_cancel()
        spice.copy_ui().add_page_pop_up_cancel_yes()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)

    finally:
        # Unload media from ADF
        scan_emulation.media.load_media('ADF', 1)   
        # udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt more than 10 pages scenario with collate On
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 400
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages
        +guid:a7dac871-c3be-4e8b-bae7-ca7eb08004ef
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:400
            +test:
                +dut:
                    +type:Emulator       
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages(job, spice, cdm, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'On',
            'copies': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than 10pages
        for _ in range(9):
            spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
            spice.copy_ui().add_page_pop_up_add_more()
        
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt add more than 10 pages scenario with collate off
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 400
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages_collate_off
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages_collate_off
        +guid:5da7612b-dc09-4441-9698-e78d1c8109fe
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt   
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_1_1Sided_add_page_scan_more_than_10_pages_collate_off(job, spice, cdm, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'off',
            'copies': '3',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        # Scan more than 10pages
        for _ in range(9):
            spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
            spice.copy_ui().add_page_pop_up_add_more()
        
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
        
    finally:
        # Unload media from ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the flatbed 1_1Sided addPage prompt noResponse/timeout scenario
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-161757
    +timeout: 600
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_1_1Sided_add_page_scan_and_no_response
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_copy_1_1Sided_add_page_scan_and_no_response
        +guid:01f37a41-fa81-419e-a13e-31253acfcd38
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_1_1Sided_add_page_scan_and_no_response(job, spice, net, udw, scan_emulation):
    scan_emulation.media.unload_media('ADF')
    scan_emulation.media.load_media('Flatbed',1)
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'collate': 'off',
            'copies': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().add_page_pop_up_add_more()
        
        logging.info("Waiting for 180 seconds to inactive/timeout the add page pop up")
        time.sleep(240) 
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
        
    finally:
        # Unload media from ADF
        scan_emulation.media.load_media('ADF',1)    
        # udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the addpage prompt and validate list of media sizes and scan more than one page and done
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184266
    +timeout: 660
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_validate_media_sizes_in_add_page_prompt_then_scan_more_than_one_page_and_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:ScanMode
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_add_page_validate_media_sizes_in_add_page_prompt_then_scan_more_than_one_page_and_done
        +guid: 0b397383-a0e3-4b9e-842c-a26790ca0588
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_validate_media_sizes_in_add_page_prompt_then_scan_more_than_one_page_and_done(job, spice, cdm, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().validate_add_page_media_sizes(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Validate the Finish and Cancel Button icon in flatbed 2_1Sided addPage prompt
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-208121
    +timeout: 120
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_2_1Sided_validate_finish_and_cancel_button_icon_in_add_page_scan_prompt
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_2_1Sided_validate_finish_and_cancel_button_icon_in_add_page_scan_prompt
        +guid:92becc8b-3c3d-4c92-9e17-448482c705d0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & Copy=2Sided2To1 & ScanSettings=PromptforAdditionalPages & DeviceFunction=JamRecovery
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_2_1Sided_validate_finish_and_cancel_button_icon_in_add_page_scan_prompt(job, spice, udw, scan_emulation, configuration):
    scan_emulation.media.unload_media('ADF')
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided'
            }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        
        assert spice.wait_for(CopyAppWorkflowObjectIds.flatbed_two_sided_screen, timeout = 15.0)
        logging.info("At Duplex Add Page Pop Up")
        
        finish_button = spice.wait_for(CopyAppWorkflowObjectIds.button_duplex_add_page_finish)
        #DUNE-226760 The assert needs to be checked only for Small screen as Icons are used there
        #Currently it is only needed for Camden add any other small screens here once test is enabled for them
        if configuration.productname in ["camden"]:
            assert finish_button['icon'] == "qrc:/images/Glyph/Done.json"

        cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.button_duplex_add_page_cancel)
        if configuration.productname in ["camden"]:
            assert cancel_button['icon'] == "qrc:/images/Glyph/Cancel.json"
        spice.copy_ui().duplex_add_page_pop_up_finish()
        
        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    finally:
        # Load media from ADF
        scan_emulation.media.load_media('ADF')
        spice.goto_homescreen()
