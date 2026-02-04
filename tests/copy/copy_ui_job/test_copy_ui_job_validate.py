import logging
from dunetuf.copy.copy import *
import time


'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Test copy in and out check copy button status
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-22046
    +timeout:600
    +asset:Copy
    +test_framework:TUF
    +test_classification:System
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +name:test_copy_app_button_enable_after_reentering_app
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_copy_app_button_enable_after_reentering_app
        +guid:6a6bd1b3-62c1-42b8-b6d0-69d58b672a49
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy

    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator

        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''

def test_copy_app_button_enable_after_reentering_app(setup_teardown_with_copy_job, job, spice, udw, net, cdm, configuration):
    
    # Go To Copy App
    logging.info("Go to copy screen")
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    logging.info("Check Copy Button Enabled")
    time.sleep(2)
    copy_job_app.check_copy_action_button_enabled()
    
    # Go to HomeScreen 
    spice.goto_homescreen()

    # Go To Copy App
    logging.info("Go to copy screen")
    copy_job_app.goto_copy()
    logging.info("Check Copy Button Enabled")
    time.sleep(2)
    copy_job_app.check_copy_action_button_enabled()