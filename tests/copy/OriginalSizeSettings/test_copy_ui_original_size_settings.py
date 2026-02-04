import logging
import pytest
from dunetuf.copy.copy import *

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:To verify auto page size is disabled when ScannerInput is ADF
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-77856
    +timeout:300
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ui_job_with_adf_verify_auto_page_size_disabled
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_job_with_adf_verify_auto_page_size_disabled
        +guid:e86c09c2-59fa-4494-a0f5-e886622f03a3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator



$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_job_with_adf_verify_auto_page_size_disabled(setup_teardown_with_copy_job, spice, job, cdm, udw, net):
    job.bookmark_jobs()

    logging.info("load ADF")
    udw.mainApp.ScanMedia.loadMedia("ADF")

    logging.info("Go to Copy > moreoptions > original size > check for any")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()
    copy_job_app.goto_copy_option_original_size_screen()
    copy_job_app.verify_item_unavailable("MenuValueany")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as legal
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_legal
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_legal
        +guid: 849bedb2-5c8b-47f2-85eb-a8e30cf41052
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Legal
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator          
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_legal(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Legal'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as any
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_any
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_any
        +guid: 408482ab-b9c2-4875-8e04-c1ba9accfd2b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=AnySize & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_any(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Any'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as letter
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_letter
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_letter
        +guid: 3890eea2-3cef-43c9-b50c-af1915ae1b0a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Letter

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_letter(scan_emulation, print_emulation, cdm, spice, job, udw, net, configuration):
    job.bookmark_jobs()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Letter'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, configuration.familyname, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as a4
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_original_size_a4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_original_size_a4
        +guid: 0c76a17d-8a9c-4d7f-b03d-74ad34618eff
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A4 & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_original_size_a4(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'A4'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Envelope C5 (162x229 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_landingpage_original_size_envelope_c5
    +test:
        +title: test_copy_ui_flatbed_landingpage_original_size_envelope_c5
        +guid: 4bfc406e-5c55-4f62-8920-094eef3f86ac
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=EnvelopeC5
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_original_size_envelope_c5(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Envelope C5 (162x229 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as executive
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_original_size_executive
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_original_size_executive
        +guid: bf849419-f38f-44eb-9290-cdf8efd62662
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Executive & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_original_size_executive(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Executive'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as A6 (105x148 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_a6
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_a6
        +guid: 1947a8d2-3a90-4539-ad2d-9b12faa637e4
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=A6
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_a6(scan_emulation, print_emulation, cdm, spice, job, udw, net, configuration):
    job.bookmark_jobs()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'A6 (105x148 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, configuration.familyname, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 5x8 in.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_5x8in
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_5x8in
        +guid: a5ab7b1e-6c0c-48dd-9907-bf7d90145d8f
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=5x8

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_5x8in(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '5x8 in.'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 100x150mm
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_10x15_cm
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_10x15_cm
        +guid: 5edd0e35-b363-425e-bb42-70a4c314828e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=10x15cm & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_10x15_cm(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '100x150mm'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as a5
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_a5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_a5
        +guid: 557b3228-7b50-42bf-a05f-2a32db3943d5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=A5

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_a5(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'A5'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as jis_b5
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_original_size_b5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_original_size_b5
        +guid: ada45c99-f389-4f7f-9aff-d8b77a19e69c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=B5-JIS & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_original_size_b5(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'jis_b5'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as B6 (JIS) (128x182 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_b6
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_b6
        +guid: 16f71a0f-a600-471c-a028-a575afa7e827
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=B6-JIS

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_b6(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'B6 (JIS) (128x182 mm)'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Envelope DL (110x220 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_envelope_dl
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_envelope_dl
        +guid: e5e79a8d-808f-4e92-8baa-d47580918c02
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_envelope_dl(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Envelope DL (110x220 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 4x6 in.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_index_4x6
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_index_4x6
        +guid: bbf391f1-35e9-4767-add4-976306bee2ed
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=4x6 & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_index_4x6(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '4x6 in.'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 16K (197x273 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_16k_197x273
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_16k_197x273
        +guid: d294a806-d93f-4788-8480-9a4a611e29fa
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=16K197x273mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_16k_197x273(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '16K (197x273 mm)'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Statement (8.5x5.5 in.)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_widget_original_size_statement
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_widget_original_size_statement
        +guid: cdbc0575-60c1-4d02-97ff-0fda0cd61e3c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Statement & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_widget_original_size_statement(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Statement (8.5x5.5 in.)'
            }
        loadmedia = 'ADF'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()




"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Postcard (JIS) (100x148 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_postcard_100x148
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_postcard_100x148
        +guid: c123a125-6899-4055-b1d6-46985a4108fd
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=JapanesePostcard
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_postcard_100x148(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Postcard (JIS) (100x148 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Envelope #10 (4.1x9.5 in.)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_envelope_10
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_envelope_10
        +guid: c61beac6-24c6-411e-b8cf-8a8a57fbef9d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Envelope-10
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_envelope_10(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Envelope #10 (4.1x9.5 in.)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()




"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Envelope Monarch (3.9x7.5 in.)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_envelope_monarch
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_envelope_monarch
        +guid: c40b4858-884d-4502-8201-a2fa33e96c3a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=EnvelopeMonarch & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_envelope_monarch(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Envelope Monarch (3.9x7.5 in.)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as oficio_216x340
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_landingpage_original_size_oficio_216x340
    +test:
        +title: test_copy_ui_adf_landingpage_original_size_oficio_216x340
        +guid: dc111c03-bb00-4b99-a0f8-30723f0463ec
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Oficio216x340mm
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_landingpage_original_size_oficio_216x340(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Oficio_8_5x13_4'
            }
        loadmedia = 'ADF'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()




"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Envelope B5 (176x250 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_envelope_b5
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_envelope_b5
        +guid: 16700e1b-b81d-4db4-b497-c803ae5c1e3d
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=EnvelopeB5 & Widget=Settings & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_envelope_b5(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Envelope B5 (176x250 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 16K (195x270 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_original_size_16k_195x270
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_menupage_original_size_16k_195x270
        +guid: ee39c738-04dd-4a17-adf8-425696bd99cc
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=16K195x270mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_original_size_16k_195x270(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '16K (195x270 mm)'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 16K (184x260 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_original_size_16k_184x260
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_menupage_original_size_16k_184x260
        +guid: 235e6241-4e5f-4ff9-b39c-cf4aae947f8e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=16K184x260mm

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_original_size_16k_184x260(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '16K (184x260 mm)'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Double Postcard (JIS) (148x200 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_landingpage_original_size_double_postcard
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_landingpage_original_size_double_postcard
        +guid: b42aad88-5b1e-4948-b822-00b4b021df0c
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=DoubleJapanPostcardRotated

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_original_size_double_postcard(scan_emulation, print_emulation, cdm, spice, job, udw, net, configuration):
    job.bookmark_jobs()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Double Postcard (JIS) (148x200 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, configuration.familyname,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 2L (127x178 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_2l_127x178
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_2l_127x178
        +guid: 517643d6-4547-4f95-96bb-de254e9b5154
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=2L127x178mm
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_2l_127x178(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '2L (127x178 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as 5x7 in.
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_5x7in
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_5x7in
        +guid: dc22c88d-6586-432b-a52a-47a03f20f9b3
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=5x7 & Widget=Settings  & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_5x7in(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '5x7 in.'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as letter_8x10in
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_original_size_letter_8x10in
    +test:
        +title: test_copy_ui_adf_menupage_original_size_letter_8x10in
        +guid: 280b9178-fcc8-47ba-b3d6-a9fa4068547a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & ADFMediaSize=Letter
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_original_size_letter_8x10in(cdm, spice, job, udw, net, scan_emulation):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Letter'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as index_3x5in
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_landingpage_original_size_index_3x5in
    +test:
        +title: test_copy_ui_flatbed_landingpage_original_size_index_3x5in
        +guid: d1a68961-8ec7-4bc1-9212-a8e94c6512c7
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=3x5
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_original_size_index_3x5in(scan_emulation, print_emulation, cdm, spice, job, udw, net, configuration):
    job.bookmark_jobs()
    scan_emulation.media.unload_media(media_id='ADF')
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': '3x5 in.'
            }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, configuration.familyname,scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Japanese Envelope Chou #3 (120x235 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:420
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_envelope_chou_3
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_envelope_chou_3
        +guid: ba30216f-4b57-4f9a-85da-b0233a39736b
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=JapaneseEnvelopeChou-3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_envelope_chou_3(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Japanese Envelope Chou #3 (120x235 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as B4 (JIS) (257x364 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_widget_original_size_jis_b4
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_widget_original_size_jis_b4
        +guid: ee652360-4d3b-4666-a430-ce03945ddd33
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=B4-JIS & Widget=Settings   & UIComponent=CopyWidget
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_widget_original_size_jis_b4(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'B4 (JIS) (257x364 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'WidgetCopyPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as A3 (297x420 mm)
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_landingpage_original_size_a3
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_landingpage_original_size_a3
        +guid: 943d5589-98c2-4c2e-bf50-54e8cc50a39e
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=A3
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_original_size_a3(scan_emulation, print_emulation, cdm, spice, job, udw, net, configuration):
    scan_emulation.media.unload_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'A3 (297x420 mm)'
            }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, configuration.familyname)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as Custom
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:300
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_original_size_custom
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_menupage_original_size_custom
        +guid: ae88f0e6-8289-4421-a1ce-e959aa5df897
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=Custom
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_original_size_custom(cdm, spice, job, udw, net):
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'Custom'
            }
        loadmedia = 'Flatbed'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Flatbed Set original size as Any and copy job from UI
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_landingpage_original_size_any
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_landingpage_original_size_any
        +guid: 421a637e-8d91-47f5-bcbd-bc37f7459b1a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=AnySize

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_landingpage_original_size_any(cdm, spice, job, udw, net,scan_emulation, print_emulation, configuration):

    job.bookmark_jobs()
    try:
        scan_emulation.media.unload_media('ADF')
        options = {
            'size': 'Any'
            }
        loadmedia = 'Flatbed'
        copy_path = 'CopyLandingPage'
        spice.copy_ui().copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, familyname = configuration.familyname, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)
    finally:
        spice.goto_homescreen()
        # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
        scan_emulation.media.load_media('ADF')
        spice.wait_ready()
        print_emulation.tray.reset_trays()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: load paper in in ADF and verify if Any size option is visible in Original size
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:450
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_verify_original_size_any_unvisible
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_adf_verify_original_size_any_unvisible
        +guid: 3e8a52a0-3197-4cd0-8aa8-1b868a1ad2e7
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.disable_autouse
def test_copy_ui_adf_verify_original_size_any_unvisible(spice, job, udw, configuration):

    job.bookmark_jobs()

    original_size = 'Any'
    udw.mainApp.ScanMedia.loadMedia("ADF")
    logging.info("copy from Menu Copy app settings page")
    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()
    spice.copy_ui().goto_copy_option_original_size_screen()
    is_in_view = spice.copy_ui().is_original_size_visible_ui(original_size)
    if configuration.familyname == "enterprise":
        assert is_in_view == True, 'the current original size is visible unexpectedly on simulator'
    else:
        assert is_in_view == False, 'the current original size is visible unexpectedly on simulator'
    spice.copy_ui().back_to_scan_option_from_original_size_list()
    spice.copy_ui().back_to_landing_view()
    spice.goto_homescreen()
    spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: load paper in in ADF and verify ews setting if Any size option is visible in Original size
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:200
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ews_adf_verify_original_size_any_unvisible
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ews_adf_verify_original_size_any_unvisible
        +guid: 77eac755-dd9d-4c3e-9b78-44a422e9e3d9
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_adf_verify_original_size_any_unvisible(spice, configuration, udw,job, ews):
    job.bookmark_tickets()
    original_size = 'Any'
    udw.mainApp.ScanMedia.loadMedia("ADF")
    ews.load(ews.COPY_DEFAULT_JOB_OPTIONS_EWS_ENDPOINT)
    if configuration.familyname == "enterprise":
        assert ews.copy_ews_app.is_original_size_visible(original_size) == True, 'the current original size is visible unexpectedly on ews'
    else:
        assert ews.copy_ews_app.is_original_size_visible(original_size) == False, 'the current original size is visible unexpectedly on ews'

    ews.close_browser()
    jobticket =  job.get_newtickets()
    single_jobticket = jobticket[0]
    logging.info('Deleting one job ticket - %s', single_jobticket)
    job.delete_ticket(single_jobticket)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Select Original size as Any size and check for preview page and copy
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:350
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_any_size_and_preview
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_any_size_and_preview
        +guid: d1b81421-c3f2-4626-9efe-6dc9ff69b11a
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=AnySize

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_any_size_and_preview(spice, job, udw, net, configuration):

    job.bookmark_jobs()
    job.clear_joblog()

    logging.info("Unload ADF")
    udw.mainApp.ScanMedia.unloadMedia("ADF")

    logging.info("copy from Menu Copy app settings page")
    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()

    logging.info("Set Original size as Any")
    spice.copy_ui().select_original_size('Any')
    spice.copy_ui().check_original_size_value('Any', net)

    logging.info("Check for preview page and copy")
    spice.copy_ui().back_to_landing_view()
    spice.copy_ui().goto_preview_panel()
    adfLoaded = udw.mainApp.ScanMedia.isMediaLoaded("ADF")
    spice.copy_ui().start_copy_from_preview_panel(configuration.familyname,adfLoaded)
    spice.copy_ui().wait_for_copy_job_status_toast_or_modal(net, configuration, message='starting')

    job.wait_for_no_active_jobs()
    job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=120)

    spice.goto_homescreen()
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    udw.mainApp.ScanMedia.loadMedia("ADF")
    spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Set Any Size  with settings as original size parameter and sides set to 1-2, 1-2, 2-1, 2-2
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:600
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_flatbed_menupage_any_original_size_and_sides
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_flatbed_menupage_any_original_size_and_sides
        +guid: 10abc12b-d88c-4399-809d-47e563cfa106
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & ScannerInput=Flatbed & FlatbedMediaSize=AnySize

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_flatbed_menupage_any_original_size_and_sides(scan_emulation, spice, job, udw, net):

    job.bookmark_jobs()
    original_size = 'Any'
    scan_emulation.media.unload_media(media_id='ADF')
    logging.info("copy from Menu Copy app settings page")
    spice.copy_ui().goto_copy()
    spice.copy_ui().goto_copy_options_list()

    logging.info("Set Any Size  as original size parameter and sides set to 1-2, 1-2, 2-1, 2-2 ")
    sides = ['1_1_sided','1_2_sided','2_1_sided','2_2_sided']
    for side in sides:
        spice.copy_ui().select_copy_side(side)
        spice.copy_ui().check_copy_sides_value(side, net)

        spice.copy_ui().scroll_to_copy_option_original_size_item()
        spice.copy_ui().select_original_size(original_size)
        spice.copy_ui().check_original_size_value(original_size, net)

    spice.copy_ui().back_to_landing_view()

    spice.goto_homescreen()
    # For Simulator default scan resouce is ADF, then need to reload ADF end of testing
    scan_emulation.media.load_media(media_id='ADF')
    spice.wait_ready()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perform Copy job with setting original size as oficio_8_5x13
    +test_tier: 3
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-137387
    +timeout:360
    +asset: Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework: TUF
    +name: test_copy_ui_adf_menupage_original_size_oficio_8_5x13
    +test:
        +title: test_copy_ui_adf_menupage_original_size_oficio_8_5x13
        +guid: 7be33daa-b4e8-4e69-a1a1-338fa3935a63
        +dut:
            +type:Simulator, Emulator
            +configuration:DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & ADFMediaSize=Oficio8.5x13
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_adf_menupage_original_size_oficio_8_5x13(scan_emulation, print_emulation, cdm, spice, job, udw, net):
    scan_emulation.media.load_media(media_id='ADF')
    job.bookmark_jobs()
    try:
        copy_job_app = spice.copy_ui()
        options = {
            'size': 'oficio_8_5x13'
            }
        loadmedia = 'ADF'
        copy_path = 'MenuCopyDocumnetSettingsPage'
        copy_job_app.copy_job_ticket_general_method(loadmedia, copy_path, options, udw, net, print_emulation, scan_emulation=scan_emulation)
        job.wait_for_no_active_jobs()
        job.check_job_log_by_status_and_type_cdm(completion_state_list=[{"type": "copy", "status": "success"}],time_out=10)
    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        print_emulation.tray.reset_trays()

