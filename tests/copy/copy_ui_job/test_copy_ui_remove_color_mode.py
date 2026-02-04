import logging
from dunetuf.copy.copy import *
from dunetuf.ui.uioperations.WorkflowOperations.MenuAppWorkflowObjectIds import MenuAppWorkflowObjectIds
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.ui.uioperations.WorkflowOperations.WorkflowUILOperations.CopyAppWorkflowUILOperations import CopyAppWorkflowUILOperations
 
'''
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: To check whether color mode option is not present in Copy> Document Copy on mono products
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-167043
    +timeout:600
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProProductDev
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_remove_color_mode_from_document_copy
    +test:
        +title:test_copy_ui_remove_color_mode_from_document_copy
        +guid:b686d13a-9a16-4a9c-964d-c3c1619cb5c5
        +dut:
            +type:Simulator
            +configuration:DeviceFunction=Copy & PrintEngineMarking=Mono & EngineFirmwareFamily=Canon & DoXSupported=True
 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
 
def test_copy_ui_remove_color_mode_from_document_copy(setup_teardown_with_copy_job, job, spice, udw, net, cdm, configuration):
   
    copy_job_app = spice.copy_ui()
    copy_job_app.goto_copy()
    copy_job_app.goto_copy_options_list()

    color_option_found = False
    try:
      copy_job_app.select_color_mode(option="Color")
      color_option_found = True
      logging.error("Color option found in mono printer!")
    except:
      logging.info("Color option not present in mono printer")
    assert False == color_option_found
    
    logging.info("back to the home screen")
    copy_job_app.back_to_landing_view()
    copy_job_app.goto_menu_mainMenu()
    
'''  
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: To check whether color mode option is not present in Copy> IDcard Copy on mono products
    +test_tier:3
    +is_manual:False
    +reqid:DUNE-167043
    +timeout:600
    +asset:Copy
    +delivery_team:ProA4
    +feature_team:ProProductDev
    +test_framework:TUF
    +test_classification:System
    +name:test_copy_ui_remove_color_mode_from_idcard_copy
    +test:
        +title:test_copy_ui_remove_color_mode_from_idcard_copy
        +guid:e611d265-80a5-4463-b30b-0b1e94b2f06e
        +dut:
            +type:Simulator
            +configuration:Copy=IDCopy & PrintEngineMarking=Mono & EngineFirmwareFamily=Canon & DoXSupported=True
 
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
'''
 
def test_copy_ui_remove_color_mode_from_idcard_copy(setup_teardown_with_copy_job, job, spice, udw, net, cdm, configuration):
 
    idcopy_job_app = spice.idcard_copy_app
    logging.info("Go to id copy screen")
    idcopy_job_app.goto_idcopy()
    idcopy_job_app.goto_copy_options_list()
 
    color_option_found = False
    try:
      idcopy_job_app.goto_idcopy_option_color_screen()
      idcopy_job_app.set_idcopy_color_options(net,idcopy_color_options="Color")
      color_option_found = True
      logging.error("Color option found in mono printer!")
    except:
      logging.info("Color option not present in mono printer")
    assert False == color_option_found

    logging.info("back to the home screen")
    idcopy_job_app.back_to_landing_view()
    idcopy_job_app.goto_menu_mainMenu()
    
    