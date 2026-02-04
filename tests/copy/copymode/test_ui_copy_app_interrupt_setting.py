from dunetuf.copy.copy import Copy

from dunetuf.control.control import Control
from dunetuf.scan.ScanAction import ScanAction
from dunetuf.ui.uioperations.WorkflowOperations.CopyAppWorkflowObjectIds import CopyAppWorkflowObjectIds
from dunetuf.cdm.CdmEndpoints import CdmEndpoints

import logging

def find_constraint(constraints_json, constraint_path):
    for validator in constraints_json['validators'] :
        if validator['propertyPointer'] == constraint_path :
            return validator
    return None

def waitAndClickOnMiddle(spice, object_id):
    # Check that the button is present
    button = spice.wait_for(object_id)
    spice.validate_button(button)
    
    # Click on the button
    button.mouse_click()
    return button

def waitAndSwitchToggle(spice,object_id, is_checked):
    # Check that toggle is present
    toggle = spice.wait_for(object_id)
    spice.validate_button(toggle)

    if is_checked:
        # Wait for the switch to be enabled in ui
        spice.wait_until(lambda: toggle["checked"], timeout = 2.0)
    else:
        # Wait for the switch to be disabled in ui
        spice.wait_until(lambda: not toggle["checked"], timeout = 2.0)

    # Check that mouse area from toggle is present
    waitAndClickOnMiddle(spice, object_id + " MouseArea")
    return toggle

def waitAndSwitchToggleAssert(spice, object_id, is_checked):
    toggle = waitAndSwitchToggle(spice, object_id, is_checked)

    if is_checked:
        # Check switch is disabled after click
        spice.wait_until(lambda: not toggle["checked"], timeout = 2.0)
    else:
        # Check switch is enbled after click
        spice.wait_until(lambda: toggle["checked"], timeout = 2.0)

def waitAndValidateToggleState(spice, object_id, is_checked):
    # Check that toggle is present
    toggle = spice.wait_for(object_id)
    spice.validate_button(toggle)
    
    if is_checked:
        # Check switch is enabled in ui
        spice.wait_until(lambda: toggle["checked"], timeout = 2.0)
    else:
        # Check switch is disabled in ui
        spice.wait_until(lambda: not toggle["checked"], timeout = 2.0)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Enter settings app and change copy mode to direct copy. Verify that interrupt is autoenabled. Disable interrupt. Goto copy app and verify that interrupt is disabled.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_change_interrupt_toggle
    +test:
        +title:test_copy_ui_change_interrupt_toggle
        +guid: 894cb37b-dc2f-43b7-82d0-f98e7f449333
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_change_interrupt_toggle(setup_teardown_default_copy_mode, spice, udw, cdm, net, locale: str = "en"):
    
    copy_instance = Copy(cdm, udw)

    # Navigate to copymode in settings
    spice.homeMenuUI().goto_copymodeoptions(spice, net, locale)

    # Check via cdm the copymode is indirect.
    assert copy_instance.is_copymode_indirect()

    waitAndValidateToggleState(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=False)

    # Check that the direct copy mode button is present and click it
    direct_mode = waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_modal_direct_copy_menu_radio_button)

    # Wait until direct mode radiobutton is activated
    spice.wait_until(lambda: direct_mode["checked"], timeout = 2.0)

    # Check via cdm the copymode is direct and interrupt is enabled.
    assert copy_instance.is_copymode_direct()
    assert copy_instance.is_allow_interrupt_active()

    waitAndSwitchToggleAssert(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=True)

    # Check via cdm the interrupt is disabled.
    assert not copy_instance.is_allow_interrupt_active()

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

    # Goto CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Click copy mode button
    waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_button)

    # Check directmode radiobutton is present
    direct_mode = spice.wait_for(CopyAppWorkflowObjectIds.copymode_modal_direct_copy_menu_radio_button)
    spice.validate_button(direct_mode)
    
    # Wait until direct mode radiobutton is active
    spice.wait_until(lambda: direct_mode["checked"], timeout = 2.0)

    waitAndValidateToggleState(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=False)

    # Check via cdm the copymode has changed and its direct.
    assert copy_instance.is_copymode_direct()
    assert not copy_instance.is_copymode_indirect()

    # Check via cdm that interrupt is disabled.
    assert not copy_instance.is_allow_interrupt_active()

    # Check that the indirect copy mode button is present and click it
    waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_modal_indirect_copy_menu_radio_button)

    # Exit dialog
    waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_modal_close_button)

    # Navigate to copymode in settings
    spice.homeMenuUI().goto_copymodeoptions(spice, net, locale)

    # Validate toogle state is disabled
    waitAndValidateToggleState(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=False)

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test interrupt copy mode is disabled when copy mode is indirect by checking the constraint message is correct.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_ui_change_interrupt_constrained
    +test:
        +title:test_copy_ui_change_interrupt_constrained
        +guid:c8fe2fa4-3f55-4219-bf48-7db707129fb2
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_change_interrupt_constrained(setup_teardown_default_copy_mode, spice, udw, cdm, net):
    copy_instance = Copy(cdm, udw)

    # Goto CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)
    
    # Check via cdm the copymode is indirect.
    assert copy_instance.is_copymode_indirect()

    # Click copy mode button
    waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_button)

    # Wait for toggle and enable it (Cant enable, its constrained)
    waitAndSwitchToggle(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=False)

    # Verify constraint message
    ui_string = spice.wait_for(CopyAppWorkflowObjectIds.constraint_string_msg)["message"]
    expected_string = spice.common_operations.get_expected_translation_str_by_str_id(net,'cCopyJobsToInterrupt')
    assert expected_string in ui_string, "String mismatch"

    # Close constraint modal
    closeModal = spice.wait_for(CopyAppWorkflowObjectIds.ok_button)
    closeModal.mouse_click()

    # Check that the direct copy mode button is present and click it
    direct_copy_mode = waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_modal_direct_copy_menu_radio_button)

    # Wait until direct mode radiobutton is activated
    spice.wait_until(lambda: direct_copy_mode["checked"], timeout = 2.0)

    # Check via cdm the copymode has changed and its direct.
    assert copy_instance.is_copymode_direct()
    
    # Check via cdm that interrupt is enabled.
    assert copy_instance.is_allow_interrupt_active()

    # Wait for toggle and disable it
    waitAndSwitchToggleAssert(spice, CopyAppWorkflowObjectIds.copymode_modal_interrupt_copy_menu_radio_button, is_checked=True)

    # Check via cdm that interrupt is disabled.
    assert not copy_instance.is_allow_interrupt_active()

    # Exit copymode dialog
    waitAndClickOnMiddle(spice, CopyAppWorkflowObjectIds.copymode_modal_close_button)
    
    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test interrupt copy mode is disabled when copy mode is indirect.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +name:test_copy_interrupt_constraints_cdm
    +test:
        +title:test_copy_interrupt_constraints_cdm
        +guid: 73de5eb0-db17-4589-9f42-a8eef8fdc5eb
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_interrupt_constraints_cdm(setup_teardown_default_copy_mode, cdm, udw):
    
    # Make sure copy mode is indirect
    copy_instance = Copy(cdm, udw)
    copy_instance.set_copymode_indirect()

    # Get the constraints
    response = cdm.get(CdmEndpoints.COPY_CONFIGURATION_CONSTRAINTS_ENDPOINT)
    allow_interrupt_constraint = find_constraint(response, "allowInterrupt")
    
    # Make sure interrupt is constrained.
    assert "disabled" in allow_interrupt_constraint
    assert allow_interrupt_constraint["disabled"]["value"] == 'true'
    
    # Enable direct copy
    copy_instance.set_copymode_direct()
    
    # Get constraints again
    response = cdm.get(CdmEndpoints.COPY_CONFIGURATION_CONSTRAINTS_ENDPOINT)
    allow_interrupt_constraint = find_constraint(response, "allowInterrupt")
    
    # Make sure interrupt is not constrained.
    assert "disabled" not in allow_interrupt_constraint


FILES = {
    'PWGRASTER': 'acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c',
    'RASTERSTREAM': '85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8',
    'JPEG': '19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc'
}

"""
Submit usb print job
"""
def submitUsbPrintJob(printjob, job, usbdevice, priorityModeSessionId: str = ""):
    resource = {'src': {'usb': {}}, 'dest': {'print': {}}}
    ticketId = job.create_job_ticket(resource)
    resource = {
        'src': {
            'usb': {'path': usbdevice.upload(printjob.select_file(FILES), usbdevice.get_root('usbdisk1'))}
        },
        'dest': {
            'print': {
                'copies': 1,
                'mediaSource': 'auto',
                'mediaSize': 'na_letter_8.5x11in',
                'mediaType': 'stationery',
                'plexMode': 'simplex',
                'printQuality': 'normal',
                'colorMode': 'color'
            }
        }
    }
    job.update_job_ticket(ticketId, resource)
    jobId = job.create_job(ticketId, priorityModeSessionId = priorityModeSessionId)
    job.change_job_state(jobId, 'initialize', 'initializeProcessing')
    job.check_job_state(jobId, 'ready', 30)
    job.change_job_state(jobId, 'start', 'startProcessing')
    job.check_job_state(jobId, 'processing', 30)
    return jobId

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: A print job is sent and delayed. Meanwhile, a copy job is created without interrupt. Since we are not interrupting, we expect the print job to finish first.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files: letter-600x8-color-1p-sim.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +external_files: packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +external_files: faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
    +name:test_copy_ui_interrupt_disabled_single_page
    +test:
        +title:test_copy_ui_interrupt_disabled_single_page
        +guid: 434475df-eb87-489a-9f6b-228efe4076a1
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_interrupt_disabled_single_page(setup_teardown_interrupt_copymode, job, printjob, spice, cdm, udw):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Enable direct copy
    copy_instance = Copy(cdm, udw)
    
    # Direct copymode without interrupt
    copy_instance.set_copymode_direct()
    copy_instance.set_interrupt_disabled()
    
    # Submit copy job with low priority
    job.delay_job(20)
    networkJobId = printjob.start_print(printjob.select_file(FILES))

    # Insert media
    Control.validate_result(scan_action.load_media("MDF"))

    # Goto CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
    spice.copy_app.finish_copy()

    copyJobId = job.get_last_job_id()

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

    # Wait for completion of regular job with completion state as SUCCESS
    networkJobState = job.wait_for_job_completion_cdm(networkJobId, 120)
    assert 'success' in networkJobState, f'Unexpected final job state - {networkJobState}'

    # Wait for completion of copy with completion state as SUCCESS. There is no interruption here.
    copyJobState = job.wait_for_job_completion_cdm(copyJobId, 120)
    assert 'success' in copyJobState, f'Unexpected final job state - {copyJobState}'

    # Validate job order
    # First is the job that was created as urgent using the interruptandblocknonurgentjobs priority
    # Second is the job that was interrupted
    expectedJobOrder    = [job.get_jobid(networkJobId), job.get_jobid(copyJobId)]
    actualJobOrder      = [joblog.get('jobId') for joblog in job.get_job_history()]
    logging.info("expectedJobOrder  : %s", expectedJobOrder)
    logging.info("actualJobOrder    : %s", actualJobOrder)
    assert expectedJobOrder == actualJobOrder, 'Unexpected job log order!'


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: A print job is sent and delayed. Meanwhile, a copy job is created with interrupt. This interrupts the first job and prioritizes the copy job.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:200
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files: letter-600x8-color-1p-sim.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +external_files: packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +external_files: faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
    +name:test_copy_ui_interrupt_enabled_single_page
    +test:
        +title:test_copy_ui_interrupt_enabled_single_page
        +guid: af48efdc-87bb-4f4d-9b72-bf3fd4eade17
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_interrupt_enabled_single_page(setup_teardown_interrupt_copymode, job, printjob, spice, cdm, udw):


    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Enable direct copy
    copy_instance = Copy(cdm, udw)

    # Direct copymode with interrupt
    copy_instance.set_copymode_direct()
    copy_instance.set_interrupt_enabled()

    # Submit copy job with low priority
    job.delay_job(20)
    networkJobId = printjob.start_print(printjob.select_file(FILES))

    # Insert media
    Control.validate_result(scan_action.load_media("MDF"))

    # Goto CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Start Copy
    spice.copy_app.start_copy()
    spice.copy_ui().wait_for_acquisition_finished_and_for_copy_button_enabled(copy_instance)

    # Finish Copy
    spice.copy_app.finish_copy()

    # As an urgent job was created, check current printing job got interrupted
    job.wait_for_job_state(networkJobId, "INTERRUPTED")

    copyJobId = job.get_last_job_id()
    # Wait for completion of copy with completion state as SUCCESS because is an urgent job and interrupted the regular job
    copyJobState = job.wait_for_job_completion_cdm(copyJobId, 120)
    assert 'success' in copyJobState, f'Unexpected final job state - {copyJobState}'

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)

    # Wait for completion of regular job with completion state as SUCCESS
    networkJobState = job.wait_for_job_completion_cdm(networkJobId, 120)
    assert 'success' in networkJobState, f'Unexpected final job state - {networkJobState}'


    # Validate job order
    # First is the job that was created as urgent using the interruptandblocknonurgentjobs priority
    # Second is the high job that was interrupted
    expectedJobOrder    = [job.get_jobid(copyJobId), job.get_jobid(networkJobId)]
    actualJobOrder      = [joblog.get('jobId') for joblog in job.get_job_history()]
    logging.info("expectedJobOrder  : %s", expectedJobOrder)
    logging.info("actualJobOrder    : %s", actualJobOrder)
    assert expectedJobOrder == actualJobOrder, 'Unexpected job log order!'

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: While in copy app, without interrupt enabled, if we receive another usb job, it executes as expected, with no interruptions.
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-175542
    +timeout:120
    +asset:LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework:TUF
    +external_files: letter-600x8-color-1p-sim.pwg=acd1927984e9ed031fc4dac26cbd29112725a05e235b263aa31abdb2465c488c
    +external_files: packets_cmyk_planar_2_colors.rs=85133be57a0ba5f27efc862ee64dbcf0ddb8e0e2b1557503700de1658d50f0c8
    +external_files: faces_small.jpg=19d6b2e4af3faca6ef1c95c5750a3c8dea079b14a04a061cf4d2acdfaf2cb9fc
    +name:test_copy_ui_print_while_copy_app
    +test:
        +title:test_copy_ui_print_while_copy_app
        +guid: 44fc6178-f9c3-4785-a909-b92694cefa95
        +dut:
            +type:Simulator,Emulator
            +configuration:DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_ui_print_while_copy_app(setup_teardown_interrupt_copymode, job, printjob, usbdevice, spice, cdm, udw):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)

    # Enable direct copy
    copy_instance = Copy(cdm, udw)

    # Direct copymode without interrupt
    copy_instance.set_copymode_direct()
    copy_instance.set_interrupt_disabled()

    # Goto CopyApp
    spice.main_app.goto_copy_app()
    copy_app = spice.copy_app.get_copy_app()
    spice.copy_app.wait_locator_enabled(spice.copy_app.locators.ui_copy_app)
    spice.validate_app(copy_app, False)

    # Submit print from usb job
    usbJobId1 = submitUsbPrintJob(printjob, job, usbdevice)

    # Wait for completion of regular job with completion state as SUCCESS
    usbJobState = job.wait_for_job_completion_cdm(usbJobId1, 120)
    assert 'success' in usbJobState, f'Unexpected final job state - {usbJobState}'

    # Back Home
    spice.goto_homescreen()
    spice.main_app.wait_locator_enabled(spice.main_app.locators.ui_main_app)