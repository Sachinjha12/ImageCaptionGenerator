import logging
import pytest

@pytest.fixture(autouse=True)
def setup_teardown(ews):
    yield
    logging.info("\n EWS close the browser")
    ews.close_browser()


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Verify color mode option is not present in copy settings ews page on mono printer
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-167479
    +timeout:300
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProProductDev
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ews_no_color_mode_option_mono_printer
    +test:
        +title:test_copy_ews_no_color_mode_option_mono_printer
        +guid:ef0d5e9a-0c16-4026-9182-5d054154ab7d
        +dut:
            +type:Simulator
            +configuration:WebServices=EWS & DeviceFunction=Copy & PrintEngineMarking=Mono
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ews_no_color_mode_option_mono_printer(ews):
    ews_copy_app = ews.copy_ews_app
    logging.info("Load the default copy job setting ews page")
    ews_copy_app.load_jobs_copy_page()
    logging.info("Color Mode Option should be invisible for mono product")
    invisible = ews.copy_ews_app.verify_element_invisible(ews_copy_app.COLOR_SELECTOR_LOCATOR)
    assert invisible, "Color Mode Option is visible for mono product"
