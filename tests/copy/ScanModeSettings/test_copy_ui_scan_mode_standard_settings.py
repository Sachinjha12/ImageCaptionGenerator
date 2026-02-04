"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to false in simplex mode and load media in ADF
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_simplex_mode_with_ADF
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_simplex_mode_with_ADF
        +guid:d5332e79-ebf1-4f2d-aaa6-be7e156cd1e2
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_simplex_mode_with_ADF(job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': False
        }
        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false in simplex mode and load media in ADF
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF
        +guid: 759f910e-3633-47b7-b3bd-2f8a49c7c304
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator     
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF(job, spice, udw, cdm, scan_emulation):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy, scan_emulation=scan_emulation)
        udw.mainApp.ScanDeviceService.setNumScanPages(3)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to false for pages per sheet 2 and load media on Flatbed scan morethan one page and click on done button
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_pages_per_sheet_2_with_flatbed_scan_more_than_one_page_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_pages_per_sheet_2_with_flatbed_scan_more_than_one_page_and_done
        +guid:a2be4987-9ae9-4b22-9d8a-f814d923a1e4
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_pages_per_sheet_2_with_flatbed_scan_more_than_one_page_and_done(job, spice, udw,cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'pagesPerSheet': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': False
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        # Unload media from Flatbed
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to false for pages per sheet 2 and load media on Flatbed scan morethan one page and click on cancel button
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_for_simplex_preview_false_pages_per_sheet_2_and_cancel
    +test:
        +title: test_copy_ui_flatbed_for_simplex_preview_false_pages_per_sheet_2_and_cancel
        +guid:21d64651-5c34-4b3f-9080-f59d466ae38a
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_for_simplex_preview_false_pages_per_sheet_2_and_cancel(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'pagesPerSheet': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': False
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_cancel()
        spice.copy_ui().add_page_pop_up_cancel_yes()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    
    finally:
        # Unload media from Flatbed
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to false for pages per sheet 2 and load media on Flatbed scan one page and switch the scanner to ADF and scan one page and click on done button
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_simplex_pages_per_sheet_2_switch_scanner_after_one_page_scan_from_flatbed_to_adf
    +test:
        +title: test_copy_ui_simplex_pages_per_sheet_2_switch_scanner_after_one_page_scan_from_flatbed_to_adf
        +guid: bf3ad2d0-ed7e-4f07-ab21-fd446417667d
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_simplex_pages_per_sheet_2_switch_scanner_after_one_page_scan_from_flatbed_to_adf(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'pagesPerSheet': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': False
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        add_button = spice.wait_for("#addButton")
        assert add_button

        # Switch the scanner to ADF
        udw.mainApp.ScanMedia.loadMedia("ADF")
        add_button.mouse_click()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false load media on ADF scan one page and switch the scanner to Flatbed and scan one page and click on cancel button in duplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_done
        +guid: 3e77ed08-cd1d-46cf-ac21-3df09d3c44d3
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt & Copy=2Sided2To1
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_done(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        add_button = spice.wait_for("#addButton")
        assert add_button

        # Switch the scanner to Flatbed
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        add_button.mouse_click()

        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false load media on ADF scan one page and switch the scanner to Flatbed and scan one page and click on cancel button in duplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel
        +guid: 00ed4187-7f54-4af5-b09d-26408c611890
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt & Copy=2Sided2To1
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        add_button = spice.wait_for("#addButton")
        assert add_button

        # Switch the scanner to Flatbed
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        add_button.mouse_click()

        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_cancel()
        spice.copy_ui().add_page_pop_up_cancel_yes()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false load media on ADF and switch scanner to flatbed and check duplex prompt after adf pages scanned
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_check_duplex_prompt_and_after_adf_click_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_check_duplex_prompt_and_after_adf_click_done
        +guid:7ab3b92b-ac1d-469d-a657-fa0d0fa05567
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt 
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_with_ADF_and_switch_to_Flatbed_check_duplex_prompt_and_after_adf_click_done(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        add_button = spice.wait_for("#addButton")
        assert add_button

        # Switch the scanner to Flatbed
        udw.mainApp.ScanMedia.unloadMedia("ADF")
        add_button.mouse_click()

        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false load media on ADF scan one page and switch the scanner to Flatbed and scan one page and click on done button in simplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_done
        +guid: 94f92b74-4950-47b0-ab5f-fb2e6a196b32
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_done(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        add_button = spice.wait_for("#addButton")
        assert add_button

        # Switch the scanner to Flatbed
        udw.mainApp.ScanMedia.unloadMedia("ADF")

        add_button.mouse_click()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to false load media on ADF scan one page and switch the scanner to Flatbed and scan one page and click on cancel button in simplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel
        +guid: 30997b30-2935-4dbd-9d9e-b102bc3f0152
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_simplex_mode_with_ADF_and_switch_to_Flatbed_and_cancel(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'ADF'
        start_copy = True
        options = {
            'sides': '1_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().add_page_pop_up_add_more()

        # Switch the scanner to Flatbed
        udw.mainApp.ScanMedia.unloadMedia("ADF")

        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_cancel()
        spice.copy_ui().add_page_pop_up_cancel_yes()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true for duplex mode and pagespersheet as 2
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 300
    +asset: Copy
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed
        +guid: ea7e0b77-29d3-4fe8-8224-fe642baae629
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & FlatbedSettings=DuplexPrompt & Copy=2Sided2To1 & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed(job, spice, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'pagesPerSheet': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        # Unload media from Flatbed
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false for duplex mode and pagespersheet as 2
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed
        +guid:e768cf4f-64cf-4dd2-a8aa-ea57bbe8e0c0
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=2Sided2To1 & Copy=2PagesPerSheet
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_false_for_duplex_mode_and_pages_per_sheet_2_with_Flatbed(job, spice, udw):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = True
        options = {
            'sides': '2_1_sided',
            'pagesPerSheet': '2',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': False
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_finish()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        # Unload media from Flatbed
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to true load media on Flatbed scan more than one page and preview the images and done for simplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 360
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_done
        +guid: 89860051-82ad-48d5-93eb-dc46fc8360c0
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=ImagePreview & Copy=Collation
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator     
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_done(spice, job, udw, scan_emulation):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'sides': '1_1_sided',
            'collate': 'On',
            'copies': '3'
        }

        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy, scan_emulation=scan_emulation)

        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().verify_image_preview("#image_0")
        spice.copy_ui().start_copy_after_preview()        

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to false and preview set to true load media on Flatbed scan one page and preview the image and cancel for simplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 240
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_cancel
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_cancel
        +guid: 86ef894a-5fb8-47cb-af25-ff7074a2e0d0
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_false_and_preview_true_for_simplex_mode_with_Flatbed_and_cancel(spice, job, udw):
    try:
        job.bookmark_jobs()

        spice.goto_homescreen()
        spice.copy_ui().goto_copy_from_copyapp_at_home_screen()
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().verify_image_preview("#image_0")
        spice.copy_ui().cancel_copy_preview()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "cancelled"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to true load media on Flatbed scan one page and preview the images and click on done button for simplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_simplex_mode_with_Flatbed_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_simplex_mode_with_Flatbed_and_done
        +guid: d0e65a8f-8042-45db-8b49-4c2c296e648e
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=ImagePreview
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_simplex_mode_with_Flatbed_and_done(spice, job, udw, cdm):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'sides': '1_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy)
        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        spice.copy_ui().start_copy_after_preview()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test the ScanMode setting in copy options with Standard Document type and promptforAdditional pages set to true and preview set to true load media on Flatbed scan one page and preview the images and done for duplex mode
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-184267
    +timeout: 300
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_duplex_mode_with_Flatbed_and_done
    +test:
        +title: test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_duplex_mode_with_Flatbed_and_done
        +guid: 5b2ad6de-ffee-447f-87a4-06ee362808e5
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedSettings=DuplexPrompt & Copy=ImagePreview & Copy=2Sided2To1
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator     
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_add_page_with_standard_document_setting_and_prompt_for_additional_pages_true_and_preview_true_for_duplex_mode_with_Flatbed_and_done(spice, job, udw, cdm, scan_emulation):
    try:
        job.bookmark_jobs()
        loadMedia = 'Flatbed'
        start_copy = False
        options = {
            'sides': '2_1_sided',
            'scan_scanMode': 'standard',
            'checkBox_for_scan_mode_prompt': True
        }

        spice.goto_homescreen()
        spice.copy_ui().copy_add_page_general_method(options, udw, loadMedia, start_copy, scan_emulation=scan_emulation)

        spice.copy_ui().click_on_preview_button_in_preview_panel()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_add_more()
        spice.copy_ui().duplex_add_page_pop_up_add_more()
        spice.copy_ui().validate_add_page_prompt_media_size_list_content(cdm)
        spice.copy_ui().add_page_pop_up_done()
        spice.copy_ui().start_copy_after_preview()

        # Check the job status of copy operation performed
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    
    finally:
        udw.mainApp.ScanMedia.loadMedia("ADF")
        spice.goto_homescreen()

