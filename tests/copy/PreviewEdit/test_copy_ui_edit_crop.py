import logging
import math
import time
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.ScanAppWorkflowObjectIds import ScanAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUIXLOperations.ScanAppWorkflowUIXLOperations import ScanAppWorkflowUIXLOperations
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.control.control import Control
import dunetuf.common.commonActions as CommonActions

from dunetuf.job.job import Job


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Check proportion is kept when changing height/width while proportions are constrained.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_check_constrained_proportions
    +test:
        +title:test_copy_ui_edit_crop_check_constrained_proportions
        +guid:2b4c865e-f266-11ee-b895-7b7bd3b71dc0
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_check_constrained_proportions(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()
    assert spice.scan_settings.get_crop_checkbox_proportions()

    # ---- Change height, check changes.

    # Starting values
    width_spinbox = spice.scan_settings.get_crop_spinbox_width()

    prev_ratio = spice.scan_settings.get_crop_ratio()
    prev_br_point = spice.scan_settings.get_crop_bottomright_corner_position()

    # Decrease height with spinboxes
    spice.scan_settings.set_crop_spinbox_width(width_spinbox * 0.5)
    # Points have changed accordingly
    # Proportion is the same
    new_ratio = spice.scan_settings.get_crop_ratio()
    new_br_point = spice.scan_settings.get_crop_bottomright_corner_position()

    # Assert prev_ratio is close to ratio with a 1% ratio
    # Proportions are constrained so bottom right point should have moved
    # in X and Y axis.
    assert math.isclose(prev_ratio, new_ratio, rel_tol=0.01)
    assert math.isclose(prev_br_point[0] * 0.5, new_br_point[0], rel_tol=0.07)
    assert math.isclose(prev_br_point[1] * 0.5, new_br_point[1], rel_tol=0.07)
    assert spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.CUSTOM

    # ---- Change orientation, check values.

    # Store W,H
    prev_width = spice.scan_settings.get_crop_spinbox_width()
    prev_height = spice.scan_settings.get_crop_spinbox_height()

    # Change orientation
    spice.scan_settings.select_crop_combobox_orientation_value(ScanAppWorkflowUIXLOperations.CropOrientationValues.LANDSCAPE )

    # Get new W,H,ratio
    new_width = spice.scan_settings.get_crop_spinbox_width()
    new_height = spice.scan_settings.get_crop_spinbox_height()
    new_ratio = spice.scan_settings.get_crop_ratio()

    # Compare Values
    assert math.isclose(prev_width, new_height, rel_tol=0.01)
    assert math.isclose(prev_height, new_width, rel_tol=0.01)
    assert math.isclose(prev_ratio * new_ratio, 1, rel_tol=0.01)

    # Back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to HomeScreen cancelling job.
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Change crop width/height. Then click on do not crop and check values.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_and_reset
    +test:
        +title:test_copy_ui_edit_crop_and_reset
        +guid:55d5271a-f337-11ee-95ba-135f90cd2693
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_and_reset(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Save initial values of width and height
    initial_width = spice.scan_settings.get_crop_spinbox_width()
    initial_height = spice.scan_settings.get_crop_spinbox_height()

    # Check crop size is Do Not Crop
    assert spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.DO_NOT_CROP

    # Uncheck Constraints
    spice.scan_settings.toggle_crop_checkbox_proportions()
    # Decrease height value
    spice.scan_settings.set_crop_spinbox_height(50)
    # Change orientation
    spice.scan_settings.select_crop_combobox_orientation_value(ScanAppWorkflowUIXLOperations.CropOrientationValues.PORTRAIT)

    # Then crop size is Custom
    assert spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.CUSTOM

    # Save initial values
    tl_position = spice.scan_settings.get_crop_topleft_corner_position()
    width = spice.scan_settings.get_crop_spinbox_width()
    height = spice.scan_settings.get_crop_spinbox_height()
    orientation = spice.scan_settings.get_crop_combobox_orientation_value()

    assert width != initial_width
    assert height != initial_height

    # Select Do Not Crop mode
    spice.scan_settings.select_crop_combobox_size_value(ScanAppWorkflowUIXLOperations.CropSizeValues.DO_NOT_CROP)

    # Check that the coordinates, width, height, and orientation have been reset
    new_tl_position = spice.scan_settings.get_crop_topleft_corner_position()
    assert tl_position[0] == new_tl_position[0]
    assert tl_position[1] == new_tl_position[1]
    assert spice.scan_settings.get_crop_spinbox_width() == initial_width
    assert spice.scan_settings.get_crop_spinbox_height() == initial_height
    assert spice.scan_settings.get_crop_combobox_orientation_value() == orientation

    # Back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to HomeScreen cancelling job.
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Change crop values then hit reset button and check values have been reset.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_and_reset_with_button
    +test:
        +title:test_copy_ui_edit_crop_and_reset_with_button
        +guid:b4461858-f33d-11ee-a571-67d429e6d783
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_and_reset_with_button(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Save initial values of width and height
    initial_tl_position = spice.scan_settings.get_crop_topleft_corner_position()
    initial_br_position = spice.scan_settings.get_crop_bottomright_corner_position()
    initial_width = spice.scan_settings.get_crop_spinbox_width()
    initial_height = spice.scan_settings.get_crop_spinbox_height()
    initial_orientation = spice.scan_settings.get_crop_combobox_orientation_value()

    # Check Size is Do Not Crop
    assert spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.DO_NOT_CROP

    # Uncheck Constraints
    spice.scan_settings.toggle_crop_checkbox_proportions()
    # Decrease height value
    spice.scan_settings.set_crop_spinbox_height(50)
    # Change orientation
    spice.scan_settings.select_crop_combobox_orientation_value(ScanAppWorkflowUIXLOperations.CropOrientationValues.PORTRAIT)

    # Then Crop Mode is Custom
    assert spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.CUSTOM

    # Save initial values.
    current_br_position = spice.scan_settings.get_crop_bottomright_corner_position()
    current_width = spice.scan_settings.get_crop_spinbox_width()
    current_height = spice.scan_settings.get_crop_spinbox_height()
    current_orientation = spice.scan_settings.get_crop_combobox_orientation_value()

    assert current_br_position[0] != initial_br_position[0]
    assert current_br_position[1] != initial_br_position[1]
    assert current_width != initial_width
    assert current_height != initial_height
    assert current_orientation == initial_orientation

    # When Reset button is pressed
    spice.scan_settings.click_edit_operation_reset_button()

    # # Then the coordinates of the resizing points in the UI and spin boxes width and height go back to initial values
    new_tl_position = spice.scan_settings.get_crop_topleft_corner_position()
    assert initial_tl_position[0] == new_tl_position[0]
    assert initial_tl_position[1] == new_tl_position[1]
    assert spice.scan_settings.get_crop_spinbox_width() == initial_width
    assert spice.scan_settings.get_crop_spinbox_height() == initial_height
    assert spice.scan_settings.get_crop_combobox_orientation_value() == initial_orientation

    # Back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to HomeScreen cancelling job.
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Perfom a crop operation then cancel the whole job.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_and_cancel_job
    +test:
        +title:test_copy_ui_edit_crop_and_cancel_job
        +guid:7d9b96fe-f34a-11ee-8d82-8313971b4e7d
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_and_cancel_job(job, spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)

    # Check Size is Do Not Crop
    # Takes time to load, that's why this is not an assert.
    spice.wait_until( lambda: spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.DO_NOT_CROP)

    # Uncheck Constraints
    spice.scan_settings.toggle_crop_checkbox_proportions()
    # Decrease height value
    spice.scan_settings.set_crop_spinbox_height(80)
    # Change orientation
    spice.scan_settings.select_crop_combobox_orientation_value(ScanAppWorkflowUIXLOperations.CropOrientationValues.PORTRAIT)

    spice.scan_settings.click_on_edit_operation_done_button()

    # Check we are back to preview screen
    spice.scan_settings.wait_for_preview_n(1)

    # Cancel the edition.
    spice.scan_settings.click_on_edit_cancel_button()

    # Should be in landing
    spice.validate_app(copy_app, True)

    # Back to HomeScreen cancelling job.
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'cancelled', 'Job is Not Cancelled'



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Move the grid Crop, then change size and check that it moves back to original point.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_move_grid_then_change_size
    +test:
        +title:test_copy_ui_edit_move_grid_then_change_size
        +guid:04eb7962-f67a-11ee-b544-5fc7e4d5349c
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_move_grid_then_change_size(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Save tl initial position
    tl_initial = spice.scan_settings.get_crop_topleft_corner_position()
    # Reduce Get current height
    height = spice.scan_settings.get_crop_spinbox_height()
    spice.scan_settings.set_crop_spinbox_height(height * 0.5)
    # Change tl position
    spice.scan_settings.set_crop_gridcrop_topleft_corner_position((50, 50))

    # Slightly increase current width
    width = spice.scan_settings.get_crop_spinbox_width()
    spice.scan_settings.set_crop_spinbox_width(width + 1)

    # check tl is at initial position
    assert spice.scan_settings.get_crop_topleft_corner_position() == tl_initial

    # Back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to HomeScreen cancelling job.
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Move the grid Crop, then change size adn check it moves back to original point.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_without_changes
    +test:
        +title:test_copy_ui_edit_crop_without_changes
        +guid:e6f23dd0-f7d5-11ee-88a5-f7a96bc43b5f
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_without_changes(job, spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Finish job
    spice.copy_app.finish_copy()

    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'
    assert new_jobs[-1].get('completionState') == 'success', 'Job is Not Cancelled'


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Move the grid Crop, perform the crop. Then enter again and check that the crop area is the same.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-102561
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_crop_then_check_values
    +test:
        +title:test_copy_ui_edit_crop_then_check_values
        +guid:9337db0a-0dd3-11ef-94f7-6732bec5ecc4
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_crop_then_check_values(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Reduce Get current height and width
    height = spice.scan_settings.get_crop_spinbox_height()
    spice.scan_settings.set_crop_spinbox_height(height * 0.5)

    # Change tl position
    spice.scan_settings.set_crop_gridcrop_topleft_corner_position((75,75))

    # Save crop area position
    tl_initial = spice.scan_settings.get_crop_topleft_corner_position()
    br_initial = spice.scan_settings.get_crop_bottomright_corner_position()
    # Save width and lenght
    width_initial = spice.scan_settings.get_crop_spinbox_width()
    height_initial = spice.scan_settings.get_crop_spinbox_height()

    # Perform crop
    spice.scan_settings.click_on_edit_operation_done_button()

    # Enter crop again
    spice.scan_settings.goto_crop_view_from_edit_scren()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Get tl and br
    tl_final = spice.scan_settings.get_crop_topleft_corner_position()
    br_final = spice.scan_settings.get_crop_bottomright_corner_position()
    # Get final width height
    width_final = spice.scan_settings.get_crop_spinbox_width()
    height_final = spice.scan_settings.get_crop_spinbox_height()

    # Compare they are close
    assert math.isclose(tl_initial[0], tl_final[0], rel_tol=0.01)
    assert math.isclose(tl_initial[1], tl_final[1], rel_tol=0.01)
    assert math.isclose(br_initial[0], br_final[0], rel_tol=0.01)
    assert math.isclose(br_initial[1], br_final[1], rel_tol=0.01)
    assert math.isclose(width_initial, width_final, rel_tol=0.01)
    assert math.isclose(height_initial, height_final, rel_tol=0.01)

    # Go back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to Homescreen
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: For grayscale edition, move the grid Crop, perform the crop. Then enter again and check that the crop area is the same.
    +test_tier:1
    +is_manual:False 
    +test_classification:System
    +reqid:DUNE-208909
    +timeout:180
    +asset:Copy
    +test_framework:TUF
    +feature_team:LFP_ScannerWorkflows
    +name:test_copy_ui_edit_grayscale_crop_then_check_values
    +test:
        +title:test_copy_ui_edit_grayscale_crop_then_check_values
        +guid:441afde8-87b5-11ef-9621-e3eb36ff8925
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & ScanEngine=LightWing & Copy=ImageEdition & Copy=ImagePreview & CopyColorMode=Grayscale
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_edit_grayscale_crop_then_check_values(spice, udw, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    spice.copy_ui().select_color_mode_landing(option="Grayscale")

    # Start Copy
    spice.copy_ui().start_copy()

    # Wait for generated thumbnail
    spice.scan_settings.wait_for_preview_n(1, timeout = 120.0)
    spice.scan_settings.wait_for_preview_available( timeout = 120.0)

    # Go to crop
    spice.scan_settings.goto_crop_view()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Reduce Get current height and width
    height = spice.scan_settings.get_crop_spinbox_height()
    spice.scan_settings.set_crop_spinbox_height(height * 0.5)

    # Change tl position
    spice.scan_settings.set_crop_gridcrop_topleft_corner_position((75,75))

    # Save crop area position
    tl_initial = spice.scan_settings.get_crop_topleft_corner_position()
    br_initial = spice.scan_settings.get_crop_bottomright_corner_position()
    # Save width and lenght
    width_initial = spice.scan_settings.get_crop_spinbox_width()
    height_initial = spice.scan_settings.get_crop_spinbox_height()

    # Perform crop
    spice.scan_settings.click_on_edit_operation_done_button()

    # Enter crop again
    spice.scan_settings.goto_crop_view_from_edit_scren()
    crop_app = spice.wait_for(ScanAppWorkflowObjectIds.preview_edit_crop_screen)
    spice.validate_app(crop_app)
    spice.scan_settings.wait_crop_available()

    # Get tl and br
    tl_final = spice.scan_settings.get_crop_topleft_corner_position()
    br_final = spice.scan_settings.get_crop_bottomright_corner_position()
    # Get final width height
    width_final = spice.scan_settings.get_crop_spinbox_width()
    height_final = spice.scan_settings.get_crop_spinbox_height()

    # Compare they are close
    assert math.isclose(tl_initial[0], tl_final[0], rel_tol=0.01)
    assert math.isclose(tl_initial[1], tl_final[1], rel_tol=0.01)
    assert math.isclose(br_initial[0], br_final[0], rel_tol=0.01)
    assert math.isclose(br_initial[1], br_final[1], rel_tol=0.01)
    assert math.isclose(width_initial, width_final, rel_tol=0.01)
    assert math.isclose(height_initial, height_final, rel_tol=0.01)

    # Go back to landing
    spice.scan_settings.goto_landing_from_crop_view()

    # Back to Homescreen
    spice.copy_app.goto_home()
    spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt)

    yes_cancel_button = spice.wait_for(CopyAppWorkflowObjectIds.copy_cancel_job_warning_prompt_primary_button)
    yes_cancel_button.mouse_click()

    assert spice.wait_for(CopyAppWorkflowObjectIds.view_ui_MainApp)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter in edit view perform crop and cancel job 
    +test_tier: 3
    +is_manual: False
    +test_classification: System
    +reqid: DUNE-201653
    +timeout: 360
    +asset: Copy
    +delivery_team: WalkupApps
    +feature_team: CopySolns
    +test_framework: TUF
    +name: test_copy_ui_edit_crop_then_cancel_job
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title: test_copy_ui_edit_crop_then_cancel_job
        +guid: aaea1be4-9f92-49b2-bab4-05f987ee8681
        +dut:
            +type: Simulator
            +configuration: DeviceClass=MFP & DeviceClass=LFP & ScannerInput=ManualFeeder & DeviceFunction=Copy & Copy=ImagePreview & ImagePreview=Edit
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_edit_crop_then_cancel_job(spice, udw, job, setup_teardown_ensure_scan_media_is_loaded, setup_teardown_homescreen):
    # CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_ui().start_copy()
    spice.scan_settings.wait_for_preview_n(1)
    
    spice.scan_settings.click_on_edit_button()
    spice.scan_settings.goto_crop_view_from_edit_scren()
    spice.wait_until( lambda: spice.scan_settings.get_crop_combobox_size_value() == ScanAppWorkflowUIXLOperations.CropSizeValues.DO_NOT_CROP)
    spice.scan_settings.set_crop_spinbox_height(80)
    job.cancel_active_jobs()
    assert spice.wait_for(CopyAppWorkflowObjectIds.pre_preview_layout)
    job.wait_for_no_active_jobs()
    new_jobs = job.get_newjobs()
    assert new_jobs[-1].get('state') == 'completed', 'Job not completed'