from dunetuf.control.control import Control
from dunetuf.job.job import Job
from dunetuf.scan.ScanAction import ScanAction, ScanSimMode

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A0 with output size A4, and check that final job is created properly
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-78660
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A0_output_size_A4
    +test:
        +title: test_copy_cdm_A0_output_size_A4
        +guid: 896236c3-081c-408f-a479-229e9440335b
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A0_output_size_A4(tcl, udw, job, copy):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A0
    height = 841 # mm
    width = 1189 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "iso_a4_210x297mm",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 66,
            "outputCanvasCustomLength": 66,
            "outputCanvasAnchor": "topLeft",
            "outputCanvasOrientation": "portrait"
        }
    }
    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Restore default simulation
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A4 with output size A0, and check that final job is created properly
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-78660
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A4_output_size_A0
    +test:
        +title: test_copy_cdm_A4_output_size_A0
        +guid: 66df4db8-6884-4dd3-b8ac-8e17b25a6a9d
        +dut:
            +type:Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A4_output_size_A0(tcl, udw, job, copy):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A4
    height = 210 # mm
    width = 297 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "iso_a0_841x1189mm",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 66,
            "outputCanvasCustomLength": 66,
            "outputCanvasAnchor": "middleCenter",
            "outputCanvasOrientation": "landscape"
        }
    }
    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

    # Restore default simulation
    simulation = scan_action.reset_simulation_mode()
    Control.validate_simulation(simulation)


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A4 with output size A0, and check that final job is created properly on emulator
    +test_tier: 1
    +is_manual: True
    +test_classification:System
    +reqid: DUNE-78660
    +timeout:120
    +asset: Copy
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A4_output_size_A0_on_emulator
    +test:
        +title: test_copy_cdm_A4_output_size_A0_on_emulator
        +guid: 7e26b100-27fb-4493-805c-81d3be14d91f
        +dut:
            +type:Emulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScanEngine=LightWing
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A4_output_size_A0_on_emulator(job, copy, udw, tcl):

    # Create some instance of the common actions ScanAction class
    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A4
    height = 210 # mm
    width = 297 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "iso_a0_841x1189mm",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 66,
            "outputCanvasCustomLength": 66,
            "outputCanvasAnchor": "middleCenter",
            "outputCanvasOrientation": "landscape"
        }
    }
    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A4 with output size custom width=150mm (5.9 inch), height=250mm (9.84 inch), and check that final job is created properly
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-111279
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A4_output_size_custom_150x250mm
    +test:
        +title: test_copy_cdm_A4_output_size_custom_150x250mm
        +guid: 6f603bdd-3234-4a5c-a771-4f12e454e63c
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A4_output_size_custom_150x250mm(job, copy, udw, tcl):


    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A4
    height = 210 # mm
    width = 297 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "custom",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 150,
            "outputCanvasCustomLength": 250,
            "outputCanvasAnchor": "middleCenter",
            "outputCanvasOrientation": "landscape"
        }
    }

    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A4 with output size custom width=250mm (9.84 inch), height=350mm (13.77 inch), and check that final job is created properly
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-111279
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A4_output_size_custom_250x350mm
    +test:
        +title: test_copy_cdm_A4_output_size_custom_250x350mm
        +guid: fac284b3-3dff-4b53-87f6-4ea3fd25980e
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & EngineFirmwareFamily=Maia
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A4_output_size_custom_250x350mm(job, copy, udw, tcl):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A4
    height = 210 # mm
    width = 297 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "custom",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 250,
            "outputCanvasCustomLength": 350,
            "outputCanvasAnchor": "middleCenter",
            "outputCanvasOrientation": "landscape"
        }
    }

    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Copy an A2 with output size custom width=500mm (16.68 inch), height=500mm (16.68 inch), and check that final job is created properly
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-111279
    +timeout:120
    +asset: LFP
    +delivery_team: LFP
    +feature_team: LFP_ScannerWorkflows
    +test_framework: TUF
    +name: test_copy_cdm_A2_output_size_custom_500x500mm_using
    +test:
        +title: test_copy_cdm_A2_output_size_custom_500x500mm_using
        +guid: c60abbee-9e3d-4925-8faf-bf0c3b66e034
        +dut:
            +type: Simulator
            +configuration:PrintEngineFormat=A0 & DeviceClass=MFP & DeviceClass=LFP & DeviceFunction=Copy & ScannerInput=ManualFeeder & EngineFirmwareFamily=Maia
    +delivery_team:LFP
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_copy_cdm_A2_output_size_custom_500x500mm_using(job, copy, udw, tcl):

    scan_action = ScanAction()
    scan_action.set_udw(udw)
    scan_action.set_tcl(tcl)

    # Create configuration Scan A2
    height = 420 # mm
    width = 594 # mm

    # Get Job ID
    last_job_id = job.get_last_job_id()

    # Create and Run configuration Copy
    settings =	{
        "src": "scan",
        "color_mode": "color",
        "resolution": "e300Dpi",
        "dest": "print",
        "copies": 1,
        "output_canvas":{
            "outputCanvasMediaSize": "custom",
            "outputCanvasMediaId": "auto",
            "outputCanvasCustomWidth": 500,
            "outputCanvasCustomLength": 500,
            "outputCanvasAnchor": "middleCenter",
            "outputCanvasOrientation": "landscape"
        }
    }

    # Do one copy with the settings
    copy.copy_simulation_force_start_CDM(height, width, settings, job, scan_action)

    # Get Job ID
    job_id = job.get_last_job_id()

    # Check if the new job has been generated
    assert job_id != last_job_id, "The new job has not been generated"

    # Get status job
    status_job = job.get_status_job(job_id)

    # Check if status is completion and success
    assert status_job[1] == "COMPLETED", "Process Status is not completed"
    assert status_job[2] == "SUCCESS", "Process Status is not success"
