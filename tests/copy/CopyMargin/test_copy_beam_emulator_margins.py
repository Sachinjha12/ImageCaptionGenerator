import logging
import pytest
from time import sleep

from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.ui.uioperations.WorkflowOperations.MediaAppWorkflowObjectIds import MediaAppWorkflowObjectIds
from dunetuf.image.PlanePosition import PlanePosition
from dunetuf.image.ImageMarginUtils import ImageMarginUtils
from dunetuf.image.JobPipelineImageCapture import JobPipelineImageCapture
from tests.copy.beam_emulator.test_copy_helpers import wait_for_print_to_complete
from dunetuf.engine.sirius.MediaSirius import MediaSirius

# Got margins by checking the output of the pipeline;
# Check src/test/dunetuf/dunetuf/tests/image/resources/imageprocessor_output.jpeg for reference.
EXPECTED_INNER_MARGINS = (PlanePosition(23.5,21.5), PlanePosition(2337.5,21.5), PlanePosition(23.5,3223.5), PlanePosition(2337.5,3223.5))

# Got margins by checking the input image;
# Check src/fw/scan/ScanRPC/FormatterToScanner/SimulatorBeam/resources/all/scan.jpg for reference.
EXPECTED_INNER_MARGINS_ADD_CONTENTS = (PlanePosition(82.5,80.5), PlanePosition(2396.5,80.5), PlanePosition(82.5,3282.5), PlanePosition(2396.5,3282.5))

@pytest.fixture
def imageprocessor_pipeline(udw, ssh, scp):
    # init
    logging.info('-- SETUP imageprocessor_pipeline --')
    logging.info("Initializing ImageProcessor capture...")
    pipeline_output = JobPipelineImageCapture("ImageProcessorOutput", udw, ssh, scp)

    # run the tests
    yield pipeline_output

    # free
    logging.info('-- TEARDOWN imageprocessor_pipeline --')
    logging.info("Destroying ImageProcessor capture instance...")
    pipeline_output.clear()
    pipeline_output.destroy()
    
@pytest.fixture
def copy_screen_with_roll_loaded_setup(copy_screen_setup, siriusEngine, spice):
    logging.info('-- SETUP copy_screen_with_roll_loaded_setup --')
    # we need a 36" roll loaded
    siriusEngine.media.set_media_loaded(MediaSirius.Tray.MAIN_ROLL)
    
    # Click OK in the Roll Successfully Loaded screen
    spice.wait_for(MediaAppWorkflowObjectIds.load_roll_finished_ok_btn).mouse_click()

    # run the tests
    yield

    logging.info('-- TEARDOWN copy_screen_with_roll_loaded_setup --')
    # Ensure the media is unloaded after the test
    siriusEngine.media.unload_current_media()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check if Beam copies matches the margin tolerance defined.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-190920
    +timeout:300
    +asset:UI
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_margins_with_simulated_scanner_beam
    +test:
        +title:test_copy_margins_with_simulated_scanner_beam
        +guid:e0942c38-bd29-4771-a14b-d1a7e318ec37
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & ScanEngine=LFPCandela
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_margins_with_simulated_scanner_beam(copy_screen_with_roll_loaded_setup, imageprocessor_pipeline, spice, net, job, locale: str = "en-US"):
    # start copy
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)

    # wait for send
    send_scan_btn = spice.wait_for(MenuAppWorkflowObjectIds.send_scan_copy_button, timeout=8)
    send_scan_btn.mouse_click() # we're done

    # complete copy
    finish_btn, _ = wait_for_print_to_complete("cCopyCompleteMessage", spice, net, locale)
    finish_btn.mouse_click()

    # get the printed image
    img = imageprocessor_pipeline.get_latest_image_black_and_white()
    assert img is not None, "Image was not found on the remote path"
    
    # does the size make sense?
    logging.info("Checking image size...")
    width,height = img.size
    original_width,original_height = (2480,3508) # the original size was an A4
    pixels_per_mm = 12 # 300ppi ~ 12 pixels/mm
    assert original_width > width and original_height > height, \
            f"Expected smaller image than original, got otherwise instead.\nOriginal: ({original_width}x{original_height})\nGot: ({width}x{height})"
    # the delta is the trimmed pixels, /2 as it's on both sides, finally convert pixels to mm
    horizontal_mm_trimmed_per_side = ((original_width - width) / 2) / pixels_per_mm
    vertical_mm_trimmed_per_side = ((original_height - height) / 2) / pixels_per_mm
    assert horizontal_mm_trimmed_per_side < 6, \
            f"Expected less than 6mm trimmed on one horizontal side, got otherwise instead.\nOriginal: ({original_width}x{original_height})\nGot: ({width}x{height})"
    assert vertical_mm_trimmed_per_side < 6, \
            f"Expected less than 6mm trimmed on one vertical side, got otherwise instead.\nOriginal: ({original_width}x{original_height})\nGot: ({width}x{height})"
    logging.info(f"Margins OK. Horizontal: {horizontal_mm_trimmed_per_side:.2f}mm/side, vertical: {vertical_mm_trimmed_per_side:.2f}mm/side")

    # check inner margins
    logging.info("Checking inner corners...")
    offset_margins = ImageMarginUtils.get_inner_corners_diff(img, EXPECTED_INNER_MARGINS)
    logging.info(f"Margins difference got: {offset_margins} pixels")

    assert offset_margins < pixels_per_mm, \
            f"Got print image offset higher than 1mm.\n  Got corners position: {ImageMarginUtils.check_inner_corners(img)}\n  Expected corners position: {EXPECTED_INNER_MARGINS}"



"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Check if Beam copies while resizing and custom margins matches the margin tolerance defined.
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-190920
    +timeout:400
    +asset:UI
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_margins_a3_add_margins_to_contents_with_simulated_scanner_beam
    +test:
        +title:test_copy_margins_a3_add_margins_to_contents_with_simulated_scanner_beam
        +guid:719fa79c-5299-458a-9e6b-073b6b376214
        +dut:
            +type:Emulator
            +configuration:DeviceFunction=Copy & ScanEngine=LFPCandela & CopyPrintMargins=AddToContents
    +delivery_team:LFP
    +feature_team:LFP_SOHO&SMB
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_margins_a3_add_margins_to_contents_with_simulated_scanner_beam(copy_screen_with_roll_loaded_setup, siriusEngine, imageprocessor_pipeline, spice, net, job, locale: str = "en-US"):
    # set options
    logging.info("Setting special properties...")
    spice.copy_ui().goto_copy_options_list()
    logging.info("Setting 'add margins to contents'...")
    spice.copy_ui().select_copy_margins("Add to Contents") # add margins to contents
    logging.info("Setting 'scale output to A3'...")
    spice.copy_ui().select_output_scale("a3", net) # scale to A3
    spice.copy_ui().close_option_mode()
    logging.info("Properties set. Starting copy...")

    # start copy
    spice.copy_ui().copy_button_present(spice)
    spice.copy_ui().press_copy_button(spice)

    # wait for send
    send_scan_btn = spice.wait_for(MenuAppWorkflowObjectIds.send_scan_copy_button, timeout=8)
    send_scan_btn.mouse_click() # we're done

    # complete copy
    finish_btn, _ = wait_for_print_to_complete("cCopyCompleteMessage", spice, net, locale)
    finish_btn.mouse_click()

    # get the printed image
    img = imageprocessor_pipeline.get_latest_image_black_and_white()
    assert img is not None, "Image was not found on the remote path"

    # does the size make sense?
    logging.info("Checking image size...")
    width,height = img.size
    original_width,original_height = (2480,3508) # the original size was an A4
    a3_width,a3_height = (3508,4961) # A3 size
    pixels_per_mm = 12 # 300ppi ~ 12 pixels/mm
    assert a3_width > width and a3_height > height, \
            f"Expected smaller image than original, got otherwise instead.\nOriginal: ({a3_width}x{a3_height})\nGot: ({width}x{height})"
    # the delta is the trimmed pixels, /2 as it's on both sides, finally convert pixels to mm
    horizontal_mm_trimmed_per_side = ((a3_width - width) / 2) / pixels_per_mm
    assert horizontal_mm_trimmed_per_side < 6, \
            f"Expected less than 6mm trimmed on one side, got otherwise instead.\nOriginal: ({a3_width}x{a3_height})\nGot: ({width}x{height})"
    logging.info(f"Margins OK. Horizontal: {horizontal_mm_trimmed_per_side:.2f}mm/side, vertical: undefined (to keep aspect ratio)")
    # vertical axis is limited by aspect ratio; we'll find a bit more trim
    original_ratio = original_width / original_height
    expected_height = width / original_ratio
    assert abs(expected_height - height) / pixels_per_mm < 1, \
            f"Expected less than 1mm aspect ratio difference, got otherwise instead.\nOriginal: ({original_width}x{original_height})\nGot: ({width}x{height})"


    logging.info("Checking inner corners...")

    # get the expected corners
    expected_inner_corners = EXPECTED_INNER_MARGINS_ADD_CONTENTS
    # the expected margins were calculated using an A4 at 300dpi (2480x3508)
    # we have to scale those to the image we got
    def scale(pixel):
        return PlanePosition(pixel.x/original_width * width, pixel.y/original_height * height)
    expected_inner_corners = (
        scale(expected_inner_corners[0]),
        scale(expected_inner_corners[1]),
        scale(expected_inner_corners[2]),
        scale(expected_inner_corners[3])
    )

    offset_margins = ImageMarginUtils.get_inner_corners_diff(img, expected_inner_corners)
    logging.info(f"Margins difference got: {offset_margins} pixels")

    assert offset_margins < pixels_per_mm, \
            f"Got print image offset higher than 1mm.\n  Got corners position: {ImageMarginUtils.check_inner_corners(img)}\n  Expected corners position: {expected_inner_corners}"

    
    logging.info("Checking top corners...")

    top_left_corners = ImageMarginUtils.check_corner(img, 0)
    logging.debug(f"top_left_corners: {top_left_corners}")
    top_left_expected_outer_corner = scale(PlanePosition(12.5,10.5))
    # I see that there's a small line that may make an 8th corner, we'll check for >= just in case
    assert len(top_left_corners) >= 7, \
            f"Expected 7 corners on the top-left corner; got less.\ntop_left_corners: {top_left_corners}"
    assert top_left_corners[-7].distance(top_left_expected_outer_corner) <= pixels_per_mm, \
            f"Top-left outer corner offset by >1mm. Expecting: {top_left_expected_outer_corner}, got: {top_left_corners[-7]}"

    top_right_corners = ImageMarginUtils.check_corner(img, 1)
    logging.debug(f"top_right_corners: {top_right_corners}")
    top_right_expected_outer_corner = scale(PlanePosition(2466.5,10.5))
    # I see that there's a small line that may make an 8th corner, we'll check for >= just in case
    assert len(top_right_corners) >= 7, \
            f"Expected 7 corners on the top-right corner; got less.\ntop_right_corners: {top_right_corners}"
    assert top_right_corners[-7].distance(top_right_expected_outer_corner) <= pixels_per_mm, \
            f"Top-right outer corner offset by >1mm. Expecting: {top_right_expected_outer_corner}, got: {top_right_corners[-7]}"


    logging.info("Checking bottom lines count...")

    (_1,_2,vertical_scroll_start,_3) = ImageMarginUtils._get_scroll_start(img, 3) # get the bottom-left start index; just save one from the vertical list
    vertical_pixels_list = ImageMarginUtils.get_lines(img, vertical_scroll_start)
    logging.debug(f"vertical_pixels_list: {vertical_pixels_list}")
    assert len(vertical_pixels_list) == 19, \
            f"Expected 19 rows at the bottom, got something else.\nvertical_pixels_list: {vertical_pixels_list}"