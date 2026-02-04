
from dunetuf.job.job import Job
from dunetuf.copy.copy import Copy

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test in case of print path blocked, clicking on copy should show alert
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-177998
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_alert_is_resurface_for_print_path_blocked
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_copy_ui_alert_is_resurface_for_print_path_blocked
        +guid:9c409b2a-83ec-40a4-8819-132ef7c24e4a
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_ui_alert_is_resurface_for_print_path_blocked( spice, tcl):

    tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")

    try:
        spice.wait_for("#cartridgeMissing1Window")
        spice.suppliesapp.press_alert_button("#Hide")
    except:
        print("Alert not on top")

    try:
        spice.copy_ui().goto_copy()
        spice.copy_ui().start_copy()
        # start copy
        spice.copy_ui().check_print_path_blocked(spice)

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test in case of print path blocked, clicking on idcopy should show alert
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-177998
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_idcopy_ui_alert_is_resurface_for_print_path_blocked
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:IDCopy
        +sub_feature:
        +interaction:Headed
        +test_type:Positive
    +test:
        +title:test_idcopy_ui_alert_is_resurface_for_print_path_blocked
        +guid:276864cf-9314-451f-ae32-0c541b66fa05
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder & Copy=IDCopy
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_idcopy_ui_alert_is_resurface_for_print_path_blocked( spice, tcl):

    tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")

    try:
        spice.wait_for("#cartridgeMissing1Window")
        spice.suppliesapp.press_alert_button("#Hide")
    except:
        print("Alert not on top")

    try:
        spice.idcard_copy_app.goto_idcopy()
        spice.statusCenter_dashboard_collapse()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: test in case of print path blocked, clicking on copy widget should show alert
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-177998
    +timeout:600
    +asset:Copy
    +delivery_team:WalkupApps
    +feature_team:CopySolns
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_widget_ui_alert_is_resurface_for_print_path_blocked
    +categorization:
        +segment:Platform
        +area:Copy
        +feature:CopySettings
        +sub_feature:
        +interaction:Headed
        +test_type:Negative
    +test:
        +title:test_copy_widget_ui_alert_is_resurface_for_print_path_blocked
        +guid:2edf5266-9d81-4043-9e83-b964ebad0e1e
        +dut:
            +type:Simulator
            +configuration:DeviceClass=MFP & DeviceFunction=Copy & ScannerInput=AutomaticDocumentFeeder
        
    
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_copy_widget_ui_alert_is_resurface_for_print_path_blocked( spice, tcl):

    tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS activateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")

    try:
        spice.wait_for("#cartridgeMissing1Window")
        spice.suppliesapp.press_alert_button("#Hide")
    except:
        print("Alert not on top")

    try:
        spice.statusCenter_dashboard_collapse()

    finally:
        spice.goto_homescreen()
        spice.wait_ready()
        tcl.execute("""EngineSimulatorUw executeSimulatorAction ALERTS inactivateAlert {{identification:"CARTRIDGE_MISSING",instanceId:1}}""")