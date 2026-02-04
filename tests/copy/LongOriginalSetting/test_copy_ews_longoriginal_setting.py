import logging
import time
from tests.copy.copy_ews_combination import *
from dunetuf.ews.EwsCapabilities import EwsCapability

'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:set long original and verify original type is hidden
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-119786
    +timeout:120
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +external_files:
    +test_classification:System
    +name:test_copy_ews__long_original
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ews__long_original
        +guid:fb8e498d-e878-4562-bcc0-18b1c956e8b7
        +dut:
            +type:Simulator
            +configuration:DeviceClass=LFP & DeviceFunction=Copy & EngineFirmwareFamily=DoX
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
def test_copy_ews__long_original(ews):
    ews_copy_app = ews.copy_ews_app
    logging.info("load the job copy page")
    ews_copy_app.load_jobs_copy_page()
    original_paper_type = ews_copy_app.find_element_on_page(ews_copy_app.ORIGINAL_PAPER_TYPE_SELECTOR_LOCATOR)
    assert original_paper_type is not None, "Original paper type missing"
    invisible = ews_copy_app.verify_element_invisible(ews_copy_app.LONG_ORIGINAL_TOGGLE_LOCATOR)
    assert invisible, "Long original toggle should not be visible"
