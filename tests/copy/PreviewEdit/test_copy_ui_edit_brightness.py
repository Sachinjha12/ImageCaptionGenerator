import logging
import time
import os
import zlib
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.copy.copy import Copy


def crc_file(file_path):
    """Generates the crc of a filename
    Args:
        file_path: Path to the file

    Returns:
        Crc of the file
    """

    prev = 0
    for each_line in open(file_path, "rb"):
        prev = zlib.crc32(each_line, prev)
    return "%X" % (prev & 0xFFFFFFFF)


def get_file_crc(scp, file_directory, filename):
    """Calculates the crc of a file in a printer
    Args:
        scp: scp to download the file of the printer
        file_directory: directory of the file in the printer
        filename: Name of the file
    Returns:
        crc of a file
    """

    printer_file_path = file_directory + "/" + filename
    local_path = "./output/" + filename
    scp.download(origin=printer_file_path, destination=local_path)
    preview_crc = crc_file(local_path)
    os.remove(local_path)

    return preview_crc


def check_color_map_crc(ssh, scp, job_id, expected_color_map_crcs):
    """Check the crc of the generated color map (To be applied by HW)
    Args:
        ssh: SSH to Printer to search the color map file
        scp: To get the color map file from the printer
        expected_color_map_crcs: Expected Color Map Crcs
    """

    # Find color map
    job_folder = f"/mnt/customer/jobs/{job_id}/"
    ssh_command = f"find {job_folder} -iname '*colorMaps.bin*'"
    print(str(ssh.run(ssh_command)))
    filepaths = str(ssh.run(ssh_command)).strip().split("\n")

    # Check Crc
    for index, filepath in enumerate(filepaths):
        directory, filename = os.path.split(filepath)
        print("Directory: " + directory + ", Filename: " + filename)
        color_map_crc = get_file_crc(scp, directory, filename)
        print(
            "Expected Color Map CRC: "
            + str(expected_color_map_crcs[index])
            + ", Color Map CRC: "
            + str(color_map_crc)
        )
        assert expected_color_map_crcs[index] == color_map_crc


# All the test cases in this file should be enabled in BTF, once brightness is
# enabled in UI


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perfrom brightness edit on single page
    +test_tier:3
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_single_page
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_single_page
        +guid:a7871c56-547b-4e50-ac4d-f44c4344c15b
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_single_page(
    ssh, scp, cdm, spice, udw, job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window
    spice.scan_settings.perform_brightness_edit(10)

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["A605AB98"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform brightness edit on multiple page
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_multiple_page
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_multiple_page
        +guid:d62efeac-c239-4fe8-8830-7e7b5f019716
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_multiple_page(ssh, scp, spice, udw, cdm, job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Load media
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window
    spice.scan_settings.perform_brightness_edit(10)

    # Load media
    udw.mainApp.ScanMedia.loadMedia("MDF")

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(2)
    # Open Preview Window
    spice.scan_settings.perform_brightness_edit(10)

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["A605AB98", "A605AB98"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform brightness edit on single page with mutiple value change
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_multiple_slider_value_change
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_multiple_slider_value_change
        +guid:3447ae38-9791-4347-832f-dddae911b756
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_multiple_slider_value_change(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(10)
    spice.scan_settings.click_on_brightness_slider(-1)
    spice.scan_settings.click_on_brightness_slider(-9)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["8B419C61"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform brightness edit and cancel the edit view
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_edit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_edit
        +guid:dae00678-e90a-4506-83bc-7bad6f42c6c7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_edit(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-1)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_cancel_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform brightness edit and cancel the edit view
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel
        +guid:0361f685-daf2-4aee-a7f1-91d24b26ebd3
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_brightness_cancel(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-1)
    spice.scan_settings.click_on_edit_operation_cancel_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform brightness operation -> cancel operation and cancel the edit view
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_brightness_operation_cancel_edit
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_brightness_operation_cancel_edit
        +guid:686be96d-bff2-4f9a-8a26-41cf36d2406e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_brightness_cancel_brightness_operation_cancel_edit(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-1)
    spice.scan_settings.click_on_edit_operation_cancel_button()
    spice.scan_settings.click_on_edit_cancel_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view and cancel the edit view
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_MDF_enter_cancel_edit_view
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_MDF_enter_cancel_edit_view
        +guid:4b6353f6-94ba-4b30-b8cb-91a1fc0d3b35
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_MDF_enter_cancel_edit_view(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_edit_cancel_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view and click on done the edit view
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_MDF_enter_edit_view_click_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_MDF_enter_edit_view_click_done
        +guid:7648585c-95a0-43ec-9b44-7e1a9de555ed
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_MDF_enter_edit_view_click_done(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view perform brightness and click done -> again reedit the same image and click on done
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_done
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_done
        +guid:fd3c2915-10f0-4709-b678-c72a9644bf99
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_done(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.perform_brightness_edit(10)
    spice.scan_settings.perform_brightness_edit(-5)
    spice.scan_settings.perform_brightness_edit(6)

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["301F67E"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view perform brightness and click cancel -> again reedit the same image and click on cancel
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_cancel
        +guid:b3dd2a4b-797b-4a00-8cb1-a6b65133dcd1
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_multiple_edit_view_click_cancel(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-3)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_cancel_button()

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-4)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_cancel_button()

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(2)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_cancel_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["EEA003F1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view perform brightness and click done -> again reedit the same image and click on cancel
    +test_tier:3
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-147237
    +timeout:620
    +asset:Copy
    +test_framework:TUF
    +feature_team:CopySolns
    +name:test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel
        +guid:80dd35d9-dede-4e4c-8f1a-e90059b96991
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:WalkupApps
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    #Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    # Open Preview Window

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-3)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-4)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_cancel_button()

    # Click on Copy button
    # Click done button
    spice.copy_ui().done_button_present(spice, 30)
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["9E5C2DF0"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy app perform Enter in edit view perform brightness and click done -> again reedit the same image and check the brightness value is at to edited value or not
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-168749
    +timeout: 620
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel_brightness_value_check
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:Preview
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel_brightness_value_check
        +guid: b9fcc900-eb59-4964-a1d5-67789f8bb750
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_MDF_perform_one_edit_done_one_edit_cancel_brightness_value_check(
    ssh, scp, spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))
    
    # Wait for generated thumbnail 
    spice.scan_settings.wait_for_preview_n(1)
    
    # Open Preview Window
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-7)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    # Changing brightness to 5
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    assert spice.scan_settings.get_brightness_slider_value() == -7, 'Brightness value is not -7'
    spice.scan_settings.click_on_brightness_slider(5)
    spice.scan_settings.click_on_edit_operation_done_button()

    # Changing brightness to -2
    spice.scan_settings.click_on_brightness_button()
    assert spice.scan_settings.get_brightness_slider_value() == 5, 'Brightness value is not 5'
    spice.scan_settings.click_on_brightness_slider(-2)
    spice.scan_settings.click_on_edit_operation_done_button()

    # Changing brightness to 3
    spice.scan_settings.click_on_brightness_button()
    assert spice.scan_settings.get_brightness_slider_value() == -2, 'Brightness value is not -2'
    spice.scan_settings.click_on_brightness_slider(3)
    spice.scan_settings.click_on_edit_operation_done_button()
    spice.scan_settings.click_on_edit_done_button()

    # Click on Copy button
    spice.copy_ui().done_button_present(spice, 30)
    # Click done button
    spice.copy_ui().press_done_button(spice)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is not success'

    # Check Color Map where brightness is applied
    check_color_map_crc(ssh, scp, new_jobs[-1].get("jobId"), ["2DC8BFE1"])

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter in edit view perform brightness and cancel job 
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-201653
    +timeout: 390
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_edit_brightness_then_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_edit_brightness_then_cancel_job
        +guid: f3503ff4-749b-462d-a41c-6bf0f2cdbc4e
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & Copy=ImagePreview & ImagePreview=Edit
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_brightness_then_cancel_job(
    spice, udw, job, cdm, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(Copy(cdm, udw))

    spice.scan_settings.wait_for_preview_n(1)
    
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.click_on_brightness_button()
    spice.scan_settings.click_on_brightness_slider(-7)
    job.cancel_active_jobs()
    assert spice.wait_for(CopyAppWorkflowObjectIds.pre_preview_layout)
    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
